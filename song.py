class song:
    def __init__(self, title, artist, duration, genre = None):
        self.title = title
        self.artist = artist
        self.duration = duration  # duration in seconds
        self.genre = genre

    def play(self):
        print(f"Playing '{self.title}' by {self.artist} for {self.duration} seconds.")

    def info(self):
        return f"Title: {self.title}, Artist: {self.artist}, Duration: {self.duration} seconds"