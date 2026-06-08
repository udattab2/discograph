from typing import Any

import pytest
from utils.models import Artist, Genre, Album, Track

def test_artist_model() -> None:
    row: dict[str, Any] = {"id": 1, "name": "Coldplay"}
    artist = Artist.from_row(row)
    assert artist.id == 1
    assert artist.name == "Coldplay"

def test_genre_model() -> None:
    row: dict[str, Any] = {"id": 2, "name": "Electronic"}
    genre = Genre.from_row(row)
    assert genre.id == 2
    assert genre.name == "Electronic"

def test_album_model() -> None:
    row: dict[str, Any] = {"id": 10, "name": "Parachutes", "artist_id": 1, "year": 2000, "trackcount": 10, "album_no": 1}
    album = Album.from_row(row)
    assert album.id == 10
    assert album.name == "Parachutes"
    assert album.artist_id == 1
    assert album.year == 2000
    assert album.trackcount == 10
    assert album.album_no == 1

def test_track_model() -> None:
    row: dict[str, Any] = {"id": 100, "name": "Yellow", "lyrics": "Look at the stars", "album_id": 10, "length": "4:29", "genre_id": 1, "song_no": 1}
    track = Track.from_row(row)
    assert track.id == 100
    assert track.name == "Yellow"
    assert track.lyrics == "Look at the stars"
    assert track.album_id == 10
    assert track.length == "4:29"
    assert track.genre_id == 1
    assert track.song_no == 1

def test_model_missing_field() -> None:
    # If a field is missing, it should default to None
    row: dict[str, Any] = {"id": 5, "name": "Kid A"} # artist_id is missing
    album = Album.from_row(row)
    assert album.id == 5
    assert album.name == "Kid A"
    assert album.artist_id is None

def test_model_none_row() -> None:
    with pytest.raises(ValueError, match="Row data cannot be None"):
        Artist.from_row(None)
