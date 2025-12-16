from tinytag import TinyTag

class song:
    def __init__(self, file_path):

        title, artist, duration, genre = self.extract_metadata(file_path)

        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre
        self.file_path = file_path

    def play(self):
        print(f"Playing '{self.title}' by {self.artist} for {self.duration} seconds.")

    def info(self):
        return f"Title: {self.title}, Artist: {self.artist}, Duration: {self.duration} seconds"
    
    def extract_metadata(self, file_path):
        tag = TinyTag.get(file_path)
        title = tag.title if tag.title else "Unknown Title"
        artist = tag.artist if tag.artist else "Unknown Artist"
        duration = int(tag.duration) if tag.duration else 0
        genre = tag.genre if tag.genre else "Unknown Genre"
        return title, artist, duration, genre
    
    def get_complete_file_path(self):
        return self.file_path