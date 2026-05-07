import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "modules"))

from MusicDatabase import MusicDatabase
from Music import Music


@pytest.fixture
def empty_db():
    return MusicDatabase()


@pytest.fixture
def sample_music():
    mock = MagicMock()
    mock.title = "Test Song"
    mock.artist = "Test Artist"
    mock.genre = "Rock"
    mock.year = 2020
    mock.path = "test.mp3"
    mock.duration = 180.0
    return mock


@pytest.fixture
def populated_db(sample_music):
    db = MusicDatabase()
    db.add_song(sample_music)
    return db


class TestInit:
    def test_init_empty(self):
        db = MusicDatabase()
        assert db.data.empty

    def test_init_with_valid_pickle(self):
        df = pd.DataFrame([{"title": "Song", "artist": "Artist"}])
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_pickle", return_value=df):
                db = MusicDatabase("test.pkl")
                assert not db.data.empty
                assert len(db.data) == 1

    def test_init_with_invalid_pickle(self, capsys):
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_pickle", side_effect=Exception("fail")):
                db = MusicDatabase("bad.pkl")
                captured = capsys.readouterr()
                assert "Invalid or no file" in captured.out
                assert db.data is None

    def test_init_with_nonexistent_path(self):
        with patch("os.path.exists", return_value=False):
            db = MusicDatabase("nonexistent.pkl")
            assert db.data.empty


class TestAddSong:
    def test_add_song(self, empty_db):
        music = {"title": "Test", "artist": "Artist"}
        empty_db.add_song(music)
        assert len(empty_db.data) == 1
        assert empty_db.data.iloc[0]["title"] == "Test"

    def test_add_multiple_songs(self, empty_db, sample_music):
        empty_db.add_song(sample_music)
        empty_db.add_song(sample_music)
        assert len(empty_db.data) == 2


class TestRemoveSongByName:
    def test_remove_existing_song(self, capsys):
        music = MagicMock()
        music.title = "To Remove"
        db = MusicDatabase()
        db.data = pd.DataFrame([{"Title": "To Remove"}, {"Title": "Keep"}])
        db.remove_song_by_name("To Remove")
        assert len(db.data) == 1
        assert db.data.iloc[0]["Title"] == "Keep"

    def test_remove_nonexistent_song(self, capsys):
        db = MusicDatabase()
        db.data = pd.DataFrame([{"Title": "Song"}])
        db.remove_song_by_name("Not Found")
        captured = capsys.readouterr()
        assert "Music not found" in captured.out
        assert len(db.data) == 1

    def test_remove_without_title_column(self, capsys):
        db = MusicDatabase()
        db.data = pd.DataFrame([{"name": "Song"}])
        db.remove_song_by_name("Song")
        captured = capsys.readouterr()
        assert "Title column not found" in captured.out


class TestRemoveSongByIndex:
    def test_remove_valid_index(self, populated_db):
        populated_db.remove_song_by_index(0)
        assert len(populated_db.data) == 0

    def test_remove_invalid_index_raises(self, empty_db):
        with pytest.raises(KeyError, match="not valid"):
            empty_db.remove_song_by_index(99)


class TestSave:
    def test_save_with_filepath(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([{"title": "Song"}])
        with patch.object(pd.DataFrame, "to_pickle") as mock_to_pickle:
            db.save("output.pkl")
            mock_to_pickle.assert_called_once_with("output.pkl")

    def test_save_without_filepath_raises(self):
        db = MusicDatabase()
        with pytest.raises(Exception, match="No filepath"):
            db.save(None)


class TestSearch:
    def test_search_empty_db(self, empty_db, capsys):
        result = empty_db.search("query")
        captured = capsys.readouterr()
        assert "Database is empty" in captured.out
        assert result.empty

    def test_search_by_title(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Rock Song", "artist": "Artist1", "genre": "Rock"},
            {"title": "Pop Song", "artist": "Artist2", "genre": "Pop"},
        ])
        result = db.search("Rock", field="title")
        assert len(result) == 1
        assert result.iloc[0]["title"] == "Rock Song"

    def test_search_by_artist(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Song1", "artist": "Beatles", "genre": "Rock"},
            {"title": "Song2", "artist": "Stones", "genre": "Rock"},
        ])
        result = db.search("Beatles", field="artist")
        assert len(result) == 1
        assert result.iloc[0]["artist"] == "Beatles"

    def test_search_by_genre(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Song1", "artist": "Artist1", "genre": "Jazz"},
            {"title": "Song2", "artist": "Artist2", "genre": "Rock"},
        ])
        result = db.search("Jazz", field="genre")
        assert len(result) == 1
        assert result.iloc[0]["genre"] == "Jazz"

    def test_search_all_fields(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Song1", "artist": "Artist1", "genre": "Rock"},
            {"title": "Song2", "artist": "Artist2", "genre": "Pop"},
        ])
        result = db.search("Artist2")
        assert len(result) == 1
        assert result.iloc[0]["artist"] == "Artist2"

    def test_search_case_insensitive(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Hello World", "artist": "Artist", "genre": "Pop"},
        ])
        result = db.search("hello", field="title")
        assert len(result) == 1

    def test_search_invalid_field_raises(self):
        db = MusicDatabase()
        db.data = pd.DataFrame([
            {"title": "Song", "artist": "Artist", "genre": "Rock"},
        ])
        with pytest.raises(ValueError, match="Invalid field"):
            db.search("query", field="invalid")
