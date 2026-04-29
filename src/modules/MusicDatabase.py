import pandas as pd
import os


class MusicDatabase:
    data = None

    def __init__(self, filepath=None):
        if filepath and os.path.exists(filepath):
            try:
                self.data = pd.read_pickle(filepath)
            except:
                print("Invalid or no file")
        else:
            self.data = pd.DataFrame([])

    def add_song(self, music):
        self.data = pd.concat([self.data, pd.DataFrame([music])], ignore_index=True)

    def remove_song(self, index):
        try:
            self.data = self.data.drop(index)
            self.data = self.data.reset_index(drop=True)
        except KeyError:
            raise KeyError(f"Index entry: {index}, not valid. Cannot remove song")

    def save(self, filepath):
        if filepath:
            self.data.to_pickle(filepath)
        else:
            raise Exception("No filepath")
