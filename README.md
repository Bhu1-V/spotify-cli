# 🎵 Spotify CLI (Vibestream) Music Player

> **Status:** Day 1 Complete (3-Day Project Challenge)

Vibestream is a lightweight, terminal-based music player built in Python. It features a rich text UI, real-time audio visualization, and efficient playlist management using custom data structures.

## ✨ Features (Day 1)

<img width="1050" height="497" alt="Code_u0HQlCMgv5" src="https://github.com/user-attachments/assets/f6c50d1c-edaf-4dd0-b904-c89fafe01f81" />

* **Terminal UI:** Beautiful, dashboard-style interface powered by the `rich` library.
* **Audio Engine:** Low-latency playback using `miniaudio` with support for MP3 and WAV files.
* **Metadata Extraction:** Automatically reads song titles, artists, and genres using `tinytag`.
* **Real-Time Dashboard:** Dynamic progress bar and track timers that update live.
* **Playlist Management:** Full navigation (Next/Prev) through a queue of songs.

## 🛠️ Data Structures & Architecture

This project implements core computer science concepts to handle data efficiently:

* **Circular Doubly Linked List (`playlist.py`):** Used for the playlist queue. This allows O(1) time complexity for switching to the previous or next song and enables infinite looping of the playlist.
* **Hash Map / Dictionary (`music_library.py`):** Used to store the music library, allowing O(1) access to song objects by title.
* **Generator Coroutines (`playback_engine.py`):** Custom stream wrappers track playback time in real-time without blocking the main UI thread.

## 📂 Project Structure

```text
Spotify CLI/
├── main.py              # Entry point. Handles the UI render loop and user input.
├── music_library.py     # Manages the collection of songs (Hash Map).
├── playlist.py          # Implements the playlist logic (Doubly Linked List).
├── playback_engine.py   # Interface for the miniaudio library.
├── song.py              # Data class for song metadata.
├── songs/               # Directory to store your .mp3 or .wav files.
└── requirements.txt     # List of python dependencies.
```
