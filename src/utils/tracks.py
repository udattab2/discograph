import sqlite3
from typing import Any
from utils.helper import clear_screen, console
from utils.models import Track
import utils.lyrics as lyrics
from rich.panel import Panel
import questionary

def track_browse(nm4: sqlite3.Row, flag: int, cur: sqlite3.Cursor) -> int:		
    while True:
        clear_screen()
        if flag == 1:
            break

        album_name: str = nm4[0]
        track_count: Any = nm4[1]
        release_year: Any = nm4[2]
        album_id: Any = nm4[3]

        info_text = f"[bold cyan]{album_name.upper()}[/bold cyan]\n"
        details: list[str] = []
        if release_year:
            details.append(f"[dim]Year of Release:[/dim] {release_year}")
        if track_count:
            details.append(f"[dim]No. of Tracks:[/dim] {track_count}")
        info_text += " | ".join(details)

        console.print(Panel.fit(info_text, border_style="cyan"))

        cur.execute("SELECT id, name, lyrics, album_id, length, genre_id, song_no FROM track WHERE album_id=? ORDER BY song_no", (album_id, ))
        rows = cur.fetchall()
        tracks_list = [Track.from_row(r) for r in rows]

        # Build choices
        choices: list[questionary.Choice] = []

        for track in tracks_list:
            song_num = f"{track.song_no}. " if track.song_no else ""
            length_str = f" ({track.length})" if track.length else ""
            choices.append(
                questionary.Choice(
                    title=f"{song_num}{track.name}{length_str}",
                    value=str(track.id)
                )
            )

        choices.append(questionary.Choice(title="<- Go Back", value="back"))
        choices.append(questionary.Choice(title="<- Return to Main Menu", value="main"))

        ch3 = questionary.select(
            "Select a Track:",
            choices=choices,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if ch3 is None or ch3 == "back":
            break
        elif ch3 == "main":
            flag = 1
            break	

        # Fetch details for the selected track
        cur.execute("SELECT name, length, album_id, genre_id, lyrics FROM track WHERE id=?", (ch3, ))
        nm6 = cur.fetchone()
        if nm6:
            flag = lyrics.lyr_show(nm6, flag, cur)
        
    return flag
	
def track_src(trackres: list[Any], flag: int, cur: sqlite3.Cursor) -> int:
    while True:
        clear_screen()
        if flag == 1:
            break

        console.print(
            Panel.fit(
                "[bold cyan]SEARCH RESULTS[/bold cyan]\n"
                "[dim]Select a track to view details and lyrics[/dim]",
                border_style="cyan"
            )
        )

        if not trackres:
            console.print("[yellow]No matches found.[/yellow]")
            questionary.press_any_key_to_continue("Press any key to go back...").ask()
            break

        # Build options dynamically
        choices: list[questionary.Choice] = []

        for r in trackres:
            track = Track.from_row(r)
            # Try to fetch artist and album for search context
            cur.execute(
                "SELECT artist.name AS art_name, album.name AS alb_name "
                "FROM album JOIN artist ON album.artist_id = artist.id "
                "WHERE album.id = ?",
                (track.album_id, )
            )
            meta = cur.fetchone()
            meta_str = f" - by {meta[0]} (on {meta[1]})" if meta else ""
            choices.append(
                questionary.Choice(
                    title=f"{track.name}{meta_str}",
                    value=str(track.id)
                )
            )

        choices.append(questionary.Choice(title="<- Go Back", value="back"))
        choices.append(questionary.Choice(title="<- Return to Main Menu", value="main"))

        ch3 = questionary.select(
            "Select a Track:",
            choices=choices,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if ch3 is None or ch3 == "back":
            break
        elif ch3 == "main":
            flag = 1
            break	

        cur.execute("SELECT name, length, album_id, genre_id, lyrics FROM track WHERE id=?", (ch3, ))
        nm6 = cur.fetchone()
        if nm6:
            flag = lyrics.lyr_show(nm6, flag, cur)
        
    return flag	