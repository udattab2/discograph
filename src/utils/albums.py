import sqlite3
from typing import Optional
from utils.helper import clear_screen, console
from utils.models import Album
import utils.tracks as tracks
from rich.panel import Panel
import questionary

def alb_browse(ch0: str, nm2: Optional[sqlite3.Row], ch1: str, flag: int, cur: sqlite3.Cursor) -> int:
    while True:
        clear_screen()
        if flag == 1:
            break

        # nm2[0] represents the name of the Artist or Genre we are browsing under
        parent_name = nm2[0] if nm2 else "Unknown"
        console.print(
            Panel.fit(
                f"[bold cyan]{parent_name.upper()}[/bold cyan]\n"
                "[dim]Select an album to view its tracklist[/dim]",
                border_style="cyan"
            )
        )

        if ch0 == '1':
            # Browsing by Artist: ch1 is artist_id
            cur.execute("SELECT id, name, artist_id, year, trackcount, album_no FROM album WHERE artist_id=? ORDER BY album_no", (ch1, ))
        elif ch0 == '2':
            # Browsing by Genre: ch1 is genre_id
            cur.execute(
                "SELECT DISTINCT album.id, album.name, album.artist_id, album.year, album.trackcount, album.album_no "
                "FROM album JOIN track ON album.id=track.album_id "
                "WHERE track.genre_id=? ORDER BY album.album_no",
                (ch1, )
            )
        
        rows = cur.fetchall()
        albums_list = [Album.from_row(r) for r in rows]

        # Build options dynamically
        choices: list[questionary.Choice] = []
        for alb in albums_list:
            year_str = f" ({alb.year})" if alb.year else ""
            tracks_str = f" [{alb.trackcount} tracks]" if alb.trackcount else ""
            choices.append(
                questionary.Choice(
                    title=f"{alb.name}{year_str}{tracks_str}",
                    value=str(alb.id)
                )
            )
        
        choices.append(questionary.Choice(title="<- Go Back", value="back"))
        choices.append(questionary.Choice(title="<- Return to Main Menu", value="main"))

        ch2 = questionary.select(
            "Select an Album:",
            choices=choices,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if ch2 is None or ch2 == "back":
            break	
        elif ch2 == "main":
            flag = 1
            break	

        # Fetch details for the selected album
        cur.execute("SELECT name, trackcount, year, id FROM album WHERE id=?", (ch2, ))
        nm4 = cur.fetchone()
        if nm4:
            flag = tracks.track_browse(nm4, flag, cur)
        
    return flag