from dataclasses import dataclass
from typing import Any, Optional, Type, TypeVar, Mapping
from dataclasses import fields

T = TypeVar('T', bound='BaseModel')

@dataclass
class BaseModel:
    @classmethod
    def from_row(cls: Type[T], row: Mapping[str, Any] | None) -> T:
        """
        Constructs an instance of the class from a sqlite3.Row or dict-like object.
        """
        if row is None:
            raise ValueError("Row data cannot be None")

        # Extract names of the dataclass fields
        field_names = [f.name for f in fields(cls)]
        
        data: dict[str, Any] = {}
        for field in field_names:
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
