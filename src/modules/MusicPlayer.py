import pygame
import time

class Player:
    def __init__(self, db):
        self.db = db
        self.current_index = None
        self.is_playing = False
        self.start_time = None
        self.offset = 0  # tracks position when paused
        pygame.mixer.init()

    def load(self, index):
        """Load a song by index from the database."""
        if index < 0 or index >= len(self.db.data):
            raise IndexError(f"No song at index {index}")
        self.current_index = index
        path = self.db.data.iloc[index]["path"]
        pygame.mixer.music.load(path)
        self.offset = 0

    def play(self):
        """Play or resume current song."""
        if self.current_index is None:
            raise ValueError("No song loaded")
        pygame.mixer.music.play(start=self.offset)
        self.start_time = time.time()
        self.is_playing = True

    def pause(self):
        """Pause current song and save position."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.offset += time.time() - self.start_time
            self.is_playing = False

    def resume(self):
        """Resume from paused position."""
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.start_time = time.time()
            self.is_playing = True

    def seek(self, seconds):
        """Jump to a specific position in seconds."""
        self.offset = seconds
        if self.is_playing:
            pygame.mixer.music.play(start=self.offset)
            self.start_time = time.time()

    def skip_forward(self, seconds=10):
        """Skip forward by N seconds."""
        self.seek(self.get_position() + seconds)

    def skip_backward(self, seconds=10):
        """Skip backward by N seconds."""
        self.seek(max(0, self.get_position() - seconds))

    def next_song(self):
        """Load and play the next song in the database."""
        if self.current_index is None:
            raise ValueError("No song loaded")
        next_index = self.current_index + 1
        if next_index >= len(self.db.data):
            raise IndexError("Already at last song")
        self.load(next_index)
        self.play()

    def prev_song(self):
        """Load and play the previous song in the database."""
        if self.current_index is None:
            raise ValueError("No song loaded")
        prev_index = self.current_index - 1
        if prev_index < 0:
            raise IndexError("Already at first song")
        self.load(prev_index)
        self.play()

    def get_position(self):
        """Get current playback position in seconds."""
        if self.is_playing:
            return self.offset + (time.time() - self.start_time)
        return self.offset

    def get_current_song(self):
        """Return the current song's row from the database."""
        if self.current_index is None:
            return None
        return self.db.data.iloc[self.current_index]