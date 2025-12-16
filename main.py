from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.align import Align
import msvcrt
import time
import os
import music_library
import playlist
import song

def format_time(seconds):
    """Helper to convert seconds (float) to MM:SS string."""
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02}:{s:02}"

console = Console()

def render_vibestream_dashboard(playlist, current_song_node, playlist_head, playback_engine):
    """
    Renders the UI using the 'rich' library with a dynamic progress bar.
    """
    console.clear() 

    # --- 1. THE NOW PLAYING PANEL ---
    if current_song_node:
        song = current_song_node.song
        
        # 1. Get dynamic time values
        current_time = playback_engine.get_time()
        total_duration = song.duration if song.duration > 0 else 1  # Prevent div/0
        
        # 2. Calculate progress percentage (0.0 to 1.0)
        percent = min(current_time / total_duration, 1.0)
        
        # 3. Construct the visual bar
        bar_width = 30  # Total characters in the bar
        filled_slots = int(bar_width * percent)
        empty_slots = bar_width - filled_slots
        
        # [green]▬▬▬▬[/] [white]🔘[/] [grey]────[/]
        prog_bar = (
            f"[green]{'▬' * filled_slots}[/]"
            f"[white]🔘[/]"
            f"[grey]{'─' * empty_slots}[/]"
        )

        # 4. Format the text
        # Use format_time helper for clean MM:SS display
        time_display = f"{format_time(current_time)} / {format_time(total_duration)}"
        
        now_playing_text = f"""
        [bold white size=20]{song.title}[/]\n
        [italic cyan]{song.artist}[/]
        [dim]{song.genre}[/]\n
        {prog_bar}  {time_display}
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

    temp = playlist_head
    idx = 1
    # Limit to 5 rows to keep UI clean
    while temp and idx <= playlist.song_count: 
        # Mark the currently playing song
        is_playing = (temp == current_song_node)
        prefix = "▶" if is_playing else str(idx)
        
        # Highlight current song row
        title_style = "bold green" if is_playing else "white"
        
        queue_table.add_row(
            prefix,
            f"[{title_style}]{temp.song.title}[/]",
            temp.song.artist,
            format_time(temp.song.duration)
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

    # Start the first song
    if playlist_instance.get_current():
         # Assuming get_current() returns a Node, and we need the filepath
         first_song = playlist_instance.get_current()
         playback_engine.play(first_song)

    console.clear()
    should_quit = False

    # --- UI RENDER LOOP ---
    while not should_quit:
        # 1. Render the Dashboard
        render_vibestream_dashboard(
            playlist_instance,
            playlist_instance.current_song,
            playlist_instance.songs_head,
            playback_engine
        )

        # 2. Check for User Input (Non-Blocking)
        # msvcrt.kbhit() returns True if a key is waiting to be read
        if msvcrt.kbhit():
            # getch() reads the key. decode() converts bytes to string.
            key = msvcrt.getch().decode('utf-8').lower()
            
            if key == 'q':
                should_quit = True
            elif key == 'n':
                handle_next(playlist_instance, playback_engine)
            elif key == 'p':
                handle_prev(playlist_instance, playback_engine)
        
        # 3. Short sleep to prevent high CPU usage, but keep UI responsive
        time.sleep(0.1)

    # Cleanup
    playback_engine.stop()
    playback_engine.close()
    console.print("[bold green]Thanks for using Vibestream! Goodbye![/]")