import sqlite3
from utils.setcount import albcounter, songcounter

def test_setcount_counters() -> None:
    # Set up a private test database in memory
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
    CREATE TABLE Album (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        artist_id INTEGER,
        Year INTEGER,
        trackcount integer,
        album_no INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE Track (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        album_id INTEGER,
        genre_id INTEGER,
        length TEXT,
        song_no INTEGER,
        lyrics TEXT
    )
    """)
    
    # Insert albums without album_no
    cur.execute("INSERT INTO Album (id, name, artist_id, album_no) VALUES (1, 'Album A', 1, NULL)")
    cur.execute("INSERT INTO Album (id, name, artist_id, album_no) VALUES (2, 'Album B', 1, NULL)")
    cur.execute("INSERT INTO Album (id, name, artist_id, album_no) VALUES (3, 'Album C', 2, NULL)")
    
    # Insert tracks without song_no
    cur.execute("INSERT INTO Track (id, name, album_id, song_no) VALUES (1, 'Song 1', 1, NULL)")
    cur.execute("INSERT INTO Track (id, name, album_id, song_no) VALUES (2, 'Song 2', 1, NULL)")
    cur.execute("INSERT INTO Track (id, name, album_id, song_no) VALUES (3, 'Song 3', 2, NULL)")
    
    conn.commit()
    
    # Run counters
    albcounter(cur)
    songcounter(cur)
    conn.commit()
    
    # Verify album_no sequencing
    cur.execute("SELECT id, album_no FROM Album ORDER BY id")
    albums = cur.fetchall()
    assert albums[0][1] == 1 # Album A (Artist 1) -> 1
    assert albums[1][1] == 2 # Album B (Artist 1) -> 2
    assert albums[2][1] == 1 # Album C (Artist 2) -> 1
    
    # Verify song_no sequencing
    cur.execute("SELECT id, song_no FROM Track ORDER BY id")
    tracks = cur.fetchall()
    assert tracks[0][1] == 1 # Song 1 (Album 1) -> 1
    assert tracks[1][1] == 2 # Song 2 (Album 1) -> 2
    assert tracks[2][1] == 1 # Song 3 (Album 2) -> 1
    
    conn.close()
