class song_node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

# Make a Circular Doubly Linked List for Playlist
class playlist:
    def __init__(self, name):
        self.songs_head = None
        self.name = name
        self.song_count = 0
        self.current_song = None
        self.is_playing = False
        self.head = None
        self.tail = None

    def add_song(self, song):
        new_node = song_node(song)
        if not self.songs_head:
            self.songs_head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        self.song_count += 1

    def remove_song(self, title):
        if not self.songs_head:
            return "Playlist is empty."

        current = self.songs_head
        for _ in range(self.song_count):
            if current.song.title == title:
                if self.song_count == 1:
                    self.songs_head = None
                    self.head = None
                    self.tail = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.songs_head:
                        self.songs_head = current.next
                    if current == self.head:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = current.prev
                self.song_count -= 1
                return f"Removed '{title}' from the playlist."
            current = current.next
        return f"Song '{title}' not found in the playlist."
    
    def get_songs(self):
        songs = []
        if not self.songs_head:
            return songs

        current = self.songs_head
        for _ in range(self.song_count):
            songs.append(current.song.title)
            current = current.next
        return songs
    
    def print_playlist(self):
        if not self.songs_head:
            print("Playlist is empty.")
            return

        current = self.songs_head
        print(f"Playlist: {self.name}")
        for i in range(self.song_count):
            print(f"{i + 1}. {current.song.info()}")
            current = current.next

    def play(self):
        if not self.songs_head:
            print("Playlist is empty.")
            return

        if not self.is_playing:
            self.current_song = self.songs_head
            self.is_playing = True

        print(f"Now playing: {self.current_song.song.info()}")

    def next_song(self):
        if not self.is_playing:
            print("No song is currently playing.")
            return

        self.current_song = self.current_song.next
        print(f"Now playing: {self.current_song.song.info()}")

    def previous_song(self):
        if not self.is_playing:
            print("No song is currently playing.")
            return

        self.current_song = self.current_song.prev
        print(f"Now playing: {self.current_song.song.info()}")