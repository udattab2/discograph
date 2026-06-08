import pytest
import sqlite3
import os
from typing import Generator, Any
from unittest.mock import patch

@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    db_path = "test_run.db"
    # Ensure any previous leftover test db is removed
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create schema and insert mock data
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
    CREATE TABLE `Artist` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE `Genre` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE "Album" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT,
        `artist_id` INTEGER,
        `Year` INTEGER,
        `trackcount` integer,
        `album_no` INTEGER,
        FOREIGN KEY(`artist_id`) REFERENCES `artist`(`id`)
    )
    """)
    cur.execute("""
    CREATE TABLE "Track" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT,
        `album_id` INTEGER,
        `genre_id` INTEGER,
        `length` TEXT,
        `song_no` INTEGER,
        `lyrics` TEXT,
        FOREIGN KEY(`album_id`) REFERENCES `album`(`id`),
        FOREIGN KEY(`genre_id`) REFERENCES `genre`(`id`)
    )
    """)
    
    # Insert Mock Data
    cur.execute("INSERT INTO Artist (id, name) VALUES (1, 'Coldplay')")
    cur.execute("INSERT INTO Artist (id, name) VALUES (2, 'Radiohead')")
    
    cur.execute("INSERT INTO Genre (id, name) VALUES (1, 'Alternative Rock')")
    cur.execute("INSERT INTO Genre (id, name) VALUES (2, 'Electronic')")
    
    cur.execute("INSERT INTO Album (id, name, artist_id, Year, trackcount, album_no) VALUES (1, 'Parachutes', 1, 2000, 1, 1)")
    cur.execute("INSERT INTO Album (id, name, artist_id, Year, trackcount, album_no) VALUES (2, 'Kid A', 2, 2000, 1, 1)")
    
    cur.execute("INSERT INTO Track (id, name, album_id, genre_id, length, song_no, lyrics) VALUES (1, 'Yellow', 1, 1, '4:29', 1, 'Look at the stars')")
    cur.execute("INSERT INTO Track (id, name, album_id, genre_id, length, song_no, lyrics) VALUES (2, 'Everything in Its Right Place', 2, 2, '4:11', 1, 'Yesterday I woke up')")
    
    conn.commit()
    conn.close()
    
    # Monkeypatch sqlite3.connect to redirect "test2.db" requests to "test_run.db"
    original_connect = sqlite3.connect
    
    def mock_connect(database: str, *args: Any, **kwargs: Any) -> sqlite3.Connection:
        if database == "test2.db":
            return original_connect(db_path, *args, **kwargs)
        return original_connect(database, *args, **kwargs)
        
    with patch("sqlite3.connect", side_effect=mock_connect):
        yield
        
    # Clean up test database
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass
