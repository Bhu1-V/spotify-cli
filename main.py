from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.align import Align

import time
import os
import music_library
import playlist
import song

def format_duration(seconds):
    """Return MM:SS (or M:SS) formatted duration; safe for non-ints."""
    try:
        s = int(seconds)
    except (TypeError, ValueError):
        return str(seconds)
    minutes = s // 60
    secs = s % 60
    return f"{minutes}:{secs:02d}"

console = Console()

def render_vibestream_dashboard(playlist, current_song_node, playlist_head):
    """
    Renders the UI using the 'rich' library.
    Args:
        playlist: The playlist object.
        current_song_node: The node currently playing.
        playlist_head: The start of the linked list (to show the queue).
    """
    console.clear() # Clears screen cleanly

    # --- 1. THE NOW PLAYING PANEL ---
    if current_song_node:
        song = current_song_node.song
        
        # Create a visual progress bar (static for now)
        # In a real app, you'd calculate this based on timer
        prog_bar = "[green]▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬[/green][grey]🔘════════════[/grey]"
        
        # The content inside the box
        now_playing_text = f"""
        [bold white size=20]{song.title}[/]\n
        [italic cyan]{song.artist}[/]
        [dim]{song.genre} • {format_duration(song.duration)}[/]\n
        {prog_bar}  1:20 / {format_duration(song.duration)}
        """
        
        main_panel = Panel(
            Align.center(now_playing_text),
            title="[bold green]🎵 NOW PLAYING[/]",
            border_style="green",
            padding=(1, 2)
        )
    else:
        main_panel = Panel(Align.center("[red]No Song Playing[/]"), title="Stopped")

    # --- 2. THE PLAYLIST TABLE (The "Up Next" View) ---
    queue_table = Table(show_header=True, header_style="bold magenta", expand=True)
    queue_table.add_column("#", style="dim", width=4)
    queue_table.add_column("Title")
    queue_table.add_column("Artist")
    queue_table.add_column("Duration", justify="right")

    # Iterate through your Doubly Linked List to populate table
    # LIMITATION: Only show next 5 songs so we don't flood screen
    temp = playlist_head
    idx = 1
    while temp and idx <= 5:
        # Mark the currently playing song with a star
        prefix = "▶" if temp == current_song_node else str(idx)
        style = "bold white" if temp == current_song_node else "white"
        
        queue_table.add_row(
            prefix,
            f"[{style}]{temp.song.title}[/]",
            temp.song.artist,
            format_duration(temp.song.duration)
        )
        temp = temp.next
        idx += 1

    # --- 3. RENDER THE LAYOUT ---
    console.print(main_panel)
    console.print("\n[bold]📋 UP NEXT:[/]")
    console.print(queue_table)
    
    # --- 4. CONTROLS GUIDE ---
    console.print(
        Panel(
            Align.center("[bold] (P)rev  |  (N)ext  |  (Q)uit [/]"),
            border_style="grey30"
        )
    )

songs_folder = "songs"
should_quit = False

def handle_quit():
    global should_quit
    should_quit = True

def handle_next(playlist_instance, playback_engine):
    playback_engine.play(playlist_instance.next_song().get_complete_file_path())

def handle_prev(playlist_instance, playback_engine):
    playback_engine.play(playlist_instance.prev_song().get_complete_file_path())

if __name__ == "__main__":    # For testing purposes, create dummy song nodes and render the dashboard
    if not os.path.exists(songs_folder):
        os.makedirs(songs_folder)

    music_library_instance = music_library.music_library(songs_folder)
    playlist_instance = playlist.playlist("My Playlist")
    for song_obj in music_library_instance.get_all_songs().values():
        playlist_instance.add_song(song_obj)

    playback_engine = None
    try:
        from playback_engine import PlaybackEngine
        playback_engine = PlaybackEngine()
    except ImportError:
        console.print("[red]Error: miniaudio library is required for playback functionality.[/]")
        exit(1)

    playback_engine.play(playlist_instance.get_current())

    # UI Render Loop
    while not should_quit:
        render_vibestream_dashboard(
            playlist_instance,
            playlist_instance.current_song,
            playlist_instance.songs_head
        )

        time.sleep(0.5)  # Small delay to avoid excessive CPU usage

        # Handle user input
        if console.input("[bold yellow]Enter Command:[/] ").strip().lower() == 'q':
            handle_quit()
        elif console.input("[bold yellow]Enter Command:[/] ").strip().lower() == 'n':
            handle_next(playlist_instance, playback_engine)
        elif console.input("[bold yellow]Enter Command:[/] ").strip().lower() == 'p':
            handle_prev(playlist_instance, playback_engine)

    console.clear()
    console.print("[bold green]Thanks for using Vibestream! Goodbye![/]")
