import mutagen
import os


class Music:
    path = ""
    title = ""
    artist = ""
    genre = ""
    year = ""

    def file_type(self, file_path: str) -> int:
        """Check if file is a valid MP3 by magic bytes.
        Returns values in [0,1,2] for mp3,wav,unsupported."""
        signature_mp3 = bytes([0x49, 0x44, 0x33])
        signature_wav_start = bytes([0x52, 0x49, 0x46, 0x46])  # "RIFF"
        signature_wav_end = bytes([0x57, 0x41, 0x56, 0x45])
        with open(file_path, "rb") as f:
            header = f.read(12)
        if header[:3] == signature_mp3:
            return 0
        elif header[:4] == signature_wav_start and header[8:12] == signature_wav_end:
            return 1
        else:
            return 2

    def load_path(self, path):
        file_type = self.file_type(path)
        if file_type == 0:
            mut = mutagen.File(path)
            self.title = mut.get("TIT2").text[0] if mut.get("TIT2") else None
            self.artist = mut.get("TPE1").text[0] if mut.get("TPE1") else None
            self.genre = mut.get("TCON").text[0] if mut.get("TCON") else None
            self.year = int(str(mut.get("TDRC").text[0])) if mut.get("TDRC") else None
        elif file_type == 1:
            self.title = None
            self.artist = None
            self.genre = None
            self.year = None
        elif file_type == 2:
            raise ValueError(f"Unsupported file type for {path}. Expected .wav or .mp3")


    def __init__(self, path, title = None, artist = None, genre = None, year = None):
        self.path = path
        self.load_path(self.path)
        if title is not None:
            self.title = title
        if artist is not None:
            self.artist = artist
        if genre is not None:
            self.genre = genre
        if year is not None:
            self.year = year

    def __str__(self):
        return self.title
