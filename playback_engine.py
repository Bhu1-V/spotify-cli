import miniaudio
import os
import time

class PlaybackEngine:
    def __init__(self):
        self._device = miniaudio.PlaybackDevice()
        self._current_time = 0.0
        self._sample_rate = 44100
        self._channels = 2
        self._is_playing = False

    def play(self, filename):
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return

        # 1. Get info
        try:
            info = miniaudio.get_file_info(filename)
            self._sample_rate = info.sample_rate
            self._channels = info.nchannels
        except Exception:
            self._sample_rate = 44100
            self._channels = 2

        # 2. Stop existing
        if self._device.running:
            self._device.stop()
        
        # 3. Create and PRIME the streams
        stream = miniaudio.stream_file(filename)
        tracked_stream = self._track_stream_progress(stream)
        
        # CRITICAL FIX: We must "prime" our wrapper generator by calling next()
        # This executes the code up to the first 'yield', making it ready 
        # to accept the .send() calls from miniaudio.
        next(tracked_stream)
        
        # 4. Start
        print(f"Playing {filename}...")
        self._is_playing = True
        self._device.start(tracked_stream)

    def _track_stream_progress(self, original_stream):
        """
        Coroutine wrapper that proxies the .send() calls from miniaudio
        to the underlying file stream while tracking time.
        """
        self._current_time = 0.0
        
        # 1. Prime the underlying stream_file generator
        # miniaudio's stream_file yields an initial empty chunk to signal readiness.
        data = next(original_stream)
        
        # 2. Yield that initial data to signal OUR readiness.
        # The value we receive back from (yield data) will be the 'framecount' 
        # sent by the audio device in the next step.
        required_frames = yield data

        try:
            while True:
                # 3. Forward the requirement to the original stream
                # We send the frame count we just received to the file decoder
                data = original_stream.send(required_frames)
                
                # 4. Update Time
                if data:
                    frames = len(data) / self._channels
                    self._current_time += frames / self._sample_rate
                
                # 5. Yield data back to device and capture the NEXT requirement
                required_frames = yield data
                
        except StopIteration:
            # Handle end of file gracefully
            pass
        finally:
             self._is_playing = False

    def get_time(self):
        return self._current_time

    def stop(self):
        if self._device.running:
            self._device.stop()
            self._is_playing = False

    def close(self):
        self._device.close()