import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "modules"))

from Music import Music


@pytest.fixture
def mock_mp3_bytes():
    return bytes([0x49, 0x44, 0x33]) + b"\x00" * 9


@pytest.fixture
def mock_wav_bytes():
    return bytes([0x52, 0x49, 0x46, 0x46]) + b"\x00" * 4 + bytes([0x57, 0x41, 0x56, 0x45])


@pytest.fixture
def mock_unsupported_bytes():
    return b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


class TestFileType:
    def test_mp3_file_type(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None
        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=180.0),
        ):
            music = Music("dummy.mp3")
            result = music.file_type("dummy.mp3")
            assert result == 0

    def test_wav_file_type(self, mock_wav_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None
        with (
            patch("builtins.open", mock_open(read_data=mock_wav_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=180.0),
        ):
            music = Music("dummy.wav")
            result = music.file_type("dummy.wav")
            assert result == 1

    def test_unsupported_file_type(self, mock_unsupported_bytes):
        with patch("builtins.open", mock_open(read_data=mock_unsupported_bytes)):
            with pytest.raises(ValueError, match="Unsupported file type"):
                Music("dummy.flac")


class TestLoadPath:
    def test_load_mp3_with_metadata(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value.text = [MagicMock()]
        mock_mutagen.get.side_effect = lambda key: {
            "TIT2": MagicMock(text=["Test Title"]),
            "TPE1": MagicMock(text=["Test Artist"]),
            "TCON": MagicMock(text=["Test Genre"]),
            "TDRC": MagicMock(text=["2024"]),
        }.get(key)

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=180.0),
        ):
            music = Music("test.mp3")
            assert music.title == "Test Title"
            assert music.artist == "Test Artist"
            assert music.genre == "Test Genre"
            assert music.year == 2024
            assert music.duration == 180.0

    def test_load_mp3_without_metadata(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=120.0),
        ):
            music = Music("test.mp3")
            assert music.title is None
            assert music.artist is None
            assert music.genre is None
            assert music.year is None

    def test_load_unsupported_file_raises(self, mock_unsupported_bytes):
        with patch("builtins.open", mock_open(read_data=mock_unsupported_bytes)):
            with pytest.raises(ValueError, match="Unsupported file type"):
                Music("test.flac")

    def test_load_with_duration_error(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", side_effect=Exception("fail")),
        ):
            music = Music("test.mp3")
            assert music.duration is None


class TestGetDuration:
    def test_get_duration_mp3(self, mock_mp3_bytes):
        mock_mp3 = MagicMock()
        mock_mp3.info.length = 240.0

        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch("mutagen.mp3.MP3", return_value=mock_mp3),
        ):
            music = Music("test.mp3")
            duration = music.get_duration("test.mp3")
            assert duration == 240.0

    def test_get_duration_wav(self, mock_wav_bytes):
        mock_wave = MagicMock()
        mock_wave.info.length = 180.5

        with (
            patch("builtins.open", mock_open(read_data=mock_wav_bytes)),
            patch("mutagen.wave.WAVE", return_value=mock_wave),
        ):
            music = Music("test.wav")
            duration = music.get_duration("test.wav")
            assert duration == 180.5

    def test_get_duration_unsupported_raises(self, mock_unsupported_bytes):
        with patch("builtins.open", mock_open(read_data=mock_unsupported_bytes)):
            with pytest.raises(ValueError, match="Unsupported file type"):
                Music("test.flac")


class TestStr:
    def test_str_returns_title(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.side_effect = lambda key: {
            "TIT2": MagicMock(text=["My Song"]),
            "TPE1": MagicMock(text=["Artist"]),
            "TCON": MagicMock(text=["Rock"]),
            "TDRC": MagicMock(text=["2020"]),
        }.get(key)

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=200.0),
        ):
            music = Music("test.mp3")
            assert str(music) == "My Song"

    def test_str_returns_none_title(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=200.0),
        ):
            music = Music("test.mp3")
            assert music.title is None


class TestInitOverrides:
    def test_init_with_overrides(self, mock_mp3_bytes):
        mock_mutagen = MagicMock()
        mock_mutagen.get.return_value = None

        with (
            patch("builtins.open", mock_open(read_data=mock_mp3_bytes)),
            patch("mutagen.File", return_value=mock_mutagen),
            patch.object(Music, "get_duration", return_value=100.0),
        ):
            music = Music(
                "test.mp3",
                title="Custom Title",
                artist="Custom Artist",
                genre="Custom Genre",
                year=2025,
                duration=300.0,
            )
            assert music.title == "Custom Title"
            assert music.artist == "Custom Artist"
            assert music.genre == "Custom Genre"
            assert music.year == 2025
            assert music.duration == 300.0
