import mutagen
import os


class Music:
    path = ""
    title = ""
    artist = ""
    genre = ""
    year = ""

    def load_path(self, path):
        mut = mutagen.File(path)
        self.title = mut.get("TIT2").text[0]
        self.artist = mut.get("TPE1").text[0]
        self.genre = mut.get("TCON").text[0]
        self.year = mut.get("TDRC").text[0]

    def __init__(self, path, title=None, artist=None, genre=None, year=None):
        self.path = path
        self.load_path(self.path)
        # Overrides
        if title:
            self.title = title
        if artist:
            self.artist = artist
        if genre:
            self.genre = genre
        if year:
            self.year = year

    def __str__(self):
        return self.title
