import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "modules"))

from MusicPlayer import Player


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.data = MagicMock()
    db.data.__len__ = lambda self: 3
    db.data.iloc = MagicMock()
    db.data.iloc.__getitem__ = lambda self, idx: {
        0: {"path": "song1.mp3", "title": "Song 1"},
        1: {"path": "song2.mp3", "title": "Song 2"},
        2: {"path": "song3.mp3", "title": "Song 3"},
    }[idx]
    return db


@pytest.fixture
def player(mock_db):
    with patch("pygame.mixer.init"):
        with patch("pygame.mixer.music"):
            return Player(mock_db)


class TestInit:
    def test_init_state(self, player):
        assert player.current_index is None
        assert player.is_playing is False
        assert player.start_time is None
        assert player.offset == 0

    def test_init_calls_mixer_init(self):
        with patch("pygame.mixer.init") as mock_init:
            with patch("pygame.mixer.music"):
                Player(MagicMock())
                mock_init.assert_called_once()


class TestLoad:
    def test_load_valid_index(self, player, mock_db):
        with patch("pygame.mixer.music.load") as mock_load:
            player.load(1)
            assert player.current_index == 1
            mock_load.assert_called_once_with("song2.mp3")
            assert player.offset == 0

    def test_load_negative_index_raises(self, player):
        with pytest.raises(IndexError, match="No song at index"):
            player.load(-1)

    def test_load_out_of_bounds_index_raises(self, player, mock_db):
        mock_db.data.__len__ = lambda self: 3
        with pytest.raises(IndexError, match="No song at index"):
            player.load(5)


class TestPlay:
    def test_play_no_song_loaded_raises(self, player):
        with pytest.raises(ValueError, match="No song loaded"):
            player.play()

    def test_play_sets_state(self, player, mock_db):
        with patch("pygame.mixer.music.load"):
            with patch("pygame.mixer.music.play") as mock_play:
                with patch("time.time", return_value=100.0):
                    player.load(0)
                    player.play()
                    mock_play.assert_called_once_with(start=0)
                    assert player.is_playing is True
                    assert player.start_time == 100.0


class TestPause:
    def test_pause_sets_state(self, player):
        with patch("pygame.mixer.music.pause") as mock_pause:
            with patch("MusicPlayer.time.time", return_value=110.0):
                player.is_playing = True
                player.start_time = 100.0
                player.offset = 0
                player.pause()
                mock_pause.assert_called_once()
                assert player.is_playing is False
                assert player.offset == 10.0

    def test_pause_when_not_playing(self, player):
        with patch("pygame.mixer.music.pause") as mock_pause:
            player.is_playing = False
            player.pause()
            mock_pause.assert_not_called()


class TestResume:
    def test_resume_sets_state(self, player):
        with patch("pygame.mixer.music.unpause") as mock_unpause:
            with patch("time.time", return_value=150.0):
                player.is_playing = False
                player.resume()
                mock_unpause.assert_called_once()
                assert player.is_playing is True
                assert player.start_time == 150.0

    def test_resume_when_already_playing(self, player):
        with patch("pygame.mixer.music.unpause") as mock_unpause:
            player.is_playing = True
            player.resume()
            mock_unpause.assert_not_called()


class TestSeek:
    def test_seek_sets_offset(self, player):
        with patch("pygame.mixer.music.play") as mock_play:
            player.is_playing = True
            with patch("time.time", return_value=200.0):
                player.seek(30.0)
                assert player.offset == 30.0
                mock_play.assert_called_once_with(start=30.0)
                assert player.start_time == 200.0

    def test_seek_when_not_playing(self, player):
        with patch("pygame.mixer.music.play") as mock_play:
            player.is_playing = False
            player.seek(45.0)
            assert player.offset == 45.0
            mock_play.assert_not_called()


class TestSkipForward:
    def test_skip_forward(self, player):
        with patch("pygame.mixer.music.play"):
            with patch("time.time", return_value=100.0):
                player.is_playing = True
                player.offset = 10.0
                player.start_time = 100.0
                player.skip_forward(5)
                assert player.offset == 15.0


class TestSkipBackward:
    def test_skip_backward(self, player):
        with patch("pygame.mixer.music.play"):
            with patch("time.time", return_value=100.0):
                player.is_playing = True
                player.offset = 20.0
                player.start_time = 100.0
                player.skip_backward(5)
                assert player.offset == 15.0

    def test_skip_backward_clamps_to_zero(self, player):
        with patch("pygame.mixer.music.play"):
            with patch("time.time", return_value=100.0):
                player.is_playing = True
                player.offset = 3.0
                player.start_time = 100.0
                player.skip_backward(10)
                assert player.offset == 0


class TestNextSong:
    def test_next_song_no_song_loaded_raises(self, player):
        with pytest.raises(ValueError, match="No song loaded"):
            player.next_song()

    def test_next_song_at_last_raises(self, player, mock_db):
        with patch("pygame.mixer.music.load"):
            player.load(2)
            with pytest.raises(IndexError, match="Already at last song"):
                player.next_song()

    def test_next_song_plays(self, player, mock_db):
        with patch("pygame.mixer.music.load"):
            with patch("pygame.mixer.music.play") as mock_play:
                with patch("time.time", return_value=100.0):
                    player.load(0)
                    player.next_song()
                    assert player.current_index == 1
                    mock_play.assert_called()


class TestPrevSong:
    def test_prev_song_no_song_loaded_raises(self, player):
        with pytest.raises(ValueError, match="No song loaded"):
            player.prev_song()

    def test_prev_song_at_first_raises(self, player, mock_db):
        with patch("pygame.mixer.music.load"):
            player.load(0)
            with pytest.raises(IndexError, match="Already at first song"):
                player.prev_song()

    def test_prev_song_plays(self, player, mock_db):
        with patch("pygame.mixer.music.load"):
            with patch("pygame.mixer.music.play") as mock_play:
                with patch("time.time", return_value=100.0):
                    player.load(1)
                    player.prev_song()
                    assert player.current_index == 0
                    mock_play.assert_called()


class TestGetPosition:
    def test_get_position_when_playing(self, player):
        with patch("time.time", return_value=110.0):
            player.is_playing = True
            player.offset = 5.0
            player.start_time = 100.0
            assert player.get_position() == 15.0

    def test_get_position_when_paused(self, player):
        player.is_playing = False
        player.offset = 25.0
        assert player.get_position() == 25.0


class TestGetCurrentSong:
    def test_get_current_song_no_index(self, player):
        assert player.get_current_song() is None

    def test_get_current_song_with_index(self, player, mock_db):
        player.current_index = 1
        result = player.get_current_song()
        assert result is not None


class TestAmplify:
    def test_amplify_no_song_raises(self, player):
        with pytest.raises(ValueError, match="Aucune musique"):
            player.amplify(1.5)

    def test_amplify_sets_volume(self, player, mock_db):
        with patch("pygame.mixer.music.set_volume") as mock_set_volume:
            with patch("pygame.mixer.music.load"):
                player.load(0)
                player.amplify(0.75)
                mock_set_volume.assert_called_once_with(0.75)
