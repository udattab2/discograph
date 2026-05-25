import sqlite3
from utils.helper import clear_screen, console
import utils.tracks as tracks
from rich.panel import Panel
import questionary

def src(flag: int, cur: sqlite3.Cursor) -> int:
    clear_screen()
    console.print(
        Panel.fit(
            "[bold cyan]SEARCH DISCOGRAPHY[/bold cyan]\n"
            "[dim]Enter track title to search. Support case-insensitive partial matches.[/dim]",
            border_style="cyan"
        )
    )
    
    srchstr = questionary.text("Search For Track Name:").ask()
    if srchstr and srchstr.strip():
        # Case-insensitive partial matching
        cur.execute("SELECT id, name, lyrics, album_id, length, genre_id, song_no FROM track WHERE name LIKE ?", (f"%{srchstr}%", ))
        trackres = cur.fetchall()
        flag = tracks.track_src(trackres, flag, cur)
    return flag