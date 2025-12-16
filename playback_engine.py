import miniaudio
import os

class PlaybackEngine:
    def __init__(self):
        # Initialize the device once. 
        # It allows restarting with different streams.
        self._device = miniaudio.PlaybackDevice()

    def play(self, filename):
        """
        Plays the specified audio file. 
        If audio is already playing, it stops and switches to the new file immediately.
        """
        if not os.path.exists(filename):
            print(f"Error: File not found - {filename}")
            return

        # Stop currently playing audio if any
        if self._device.running:
            self._device.stop()

        print(f"Starting playback: {filename}")
        
        try:
            # Create a stream generator from the file
            # stream_file decodes the audio on the fly (efficient for memory)
            stream = miniaudio.stream_file(filename)
            
            # Start the device with the new stream (non-blocking)
            self._device.start(stream)
            
        except Exception as e:
            print(f"Error starting playback: {e}")

    def stop(self):
        """Stops the playback manually."""
        if self._device.running:
            self._device.stop()
            print("Playback stopped.")

    def is_playing(self):
        """Returns True if audio is currently running."""
        return self._device.running

    def close(self):
        """Release the device resources when done with the engine."""
        self._device.close()