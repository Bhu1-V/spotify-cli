class music_library:
    def __init__(self):
        self.songs = {}

    def add_song(self, song):
        self.songs[song.title] = song

    def remove_song(self, title):
        if title in self.songs:
            del self.songs[title]
    
    # get song by title or else Return the Error that song doesn't exist
    def get_song(self, title):
        if(title in self.songs):
            return self.songs[title]
        else:
            return "Error: Song doesn't exist in the library."

    def get_songs_by_artist(self, artist):
        return [song for song in self.songs.values() if song.artist == artist]

    def get_all_songs(self):
        return self.songs