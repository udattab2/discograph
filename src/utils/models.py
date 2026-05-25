from dataclasses import dataclass
from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar('T', bound='BaseModel')

class BaseModel:
    @classmethod
    def from_row(cls: Type[T], row: Any) -> T:
        """Constructs an instance of the class from a sqlite3.Row or dict-like object."""
        if row is None:
            raise ValueError("Row data cannot be None")
        # Extract fields from the row by matching dataclass field names
        fields = cls.__dataclass_fields__.keys()
        data = {}
        for field in fields:
            try:
                data[field] = row[field]
            except (KeyError, IndexError):
                data[field] = None
        return cls(**data)

@dataclass
class Artist(BaseModel):
    id: int
    name: str

@dataclass
class Genre(BaseModel):
    id: int
    name: str

@dataclass
class Album(BaseModel):
    id: int
    name: str
    artist_id: int
    year: Optional[int]
    trackcount: Optional[int]
    album_no: Optional[int]

@dataclass
class Track(BaseModel):
    id: int
    name: str
    lyrics: Optional[str]
    album_id: int
    length: Optional[str]
    genre_id: Optional[int]
    song_no: Optional[int]
