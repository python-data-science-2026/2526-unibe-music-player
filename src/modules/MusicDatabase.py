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

    def remove_song_by_name(self, music: str):
        if "Title" not in self.data.columns:
            print("Title column not found")
            return
        music_index = self.data.loc[self.data["Title"] == music].index
        if music_index.empty:
            print("Music not found")
            return
        self.data = self.data.drop(music_index).reset_index(drop=True)

    def remove_song_by_index(self, index):
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
    
    def search(self, query: str, field: str = "all") -> pd.DataFrame:
        """
        This function searches a MusicDatabase object for a certain string object. 
        It can be specified (field) whether we want to search for a song title 
        only, a genre only, artist only, or all of them (default). It returns matching results as a pd.DataFrame.
        """
        if self.data.empty:
            print("Database is empty.")
            return pd.DataFrame([])
        if field not in ["title", "genre", "artist", "all"]:
            raise ValueError("Invalid field. Expected 'title', 'genre', 'artist', or 'all'.")
        if field == "title":
            return self.data[self.data["title"].str.contains(query, case=False, na=False)]
        elif field == "genre":
            return self.data[self.data["genre"].str.contains(query, case=False, na=False)]
        elif field == "artist":
            return self.data[self.data["artist"].str.contains(query, case=False, na=False)]
        else:
            return self.data[
                self.data["title"].str.contains(query, case=False, na=False) |
                self.data["genre"].str.contains(query, case=False, na=False) |
                self.data["artist"].str.contains(query, case=False, na=False)
            ]
