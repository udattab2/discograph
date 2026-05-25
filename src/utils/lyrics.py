import sqlite3
from utils.helper import clear_screen, console
from rich.panel import Panel
import questionary

def lyr_show(nm6: sqlite3.Row, flag: int, cur: sqlite3.Cursor) -> int:
    while True:
        clear_screen()
        if flag == 1:
            break

        # nm6 has: [0] name, [1] length, [2] album_id, [3] genre_id, [4] lyrics
        song_name = nm6[0]
        length = nm6[1]
        album_id = nm6[2]
        genre_id = nm6[3]
        lyrics_text = nm6[4] if nm6[4] else "[dim]No lyrics available for this track.[/dim]"

        # Fetch relations
        cur.execute("SELECT name FROM genre WHERE id=?", (genre_id, ))
        genre_row = cur.fetchone()
        genre_name = genre_row[0] if genre_row else "Unknown"

        cur.execute("SELECT name, artist_id FROM album WHERE id=?", (album_id, ))
        album_row = cur.fetchone()
        album_name = album_row[0] if album_row else "Unknown"
        artist_id = album_row[1] if album_row else None

        artist_name = "Unknown"
        if artist_id:
            cur.execute("SELECT name FROM artist WHERE id=?", (artist_id, ))
            artist_row = cur.fetchone()
            artist_name = artist_row[0] if artist_row else "Unknown"

        metadata_content = (
            f"[bold cyan]Song:[/bold cyan] {song_name}\n"
            f"[bold cyan]Artist:[/bold cyan] {artist_name}\n"
            f"[bold cyan]Album:[/bold cyan] {album_name}\n"
            f"[bold cyan]Genre:[/bold cyan] {genre_name}\n"
            f"[bold cyan]Length:[/bold cyan] {length}\n\n"
            f"[bold green]Lyrics:[/bold green]\n"
            f"[dim]{lyrics_text}[/dim]"
        )

        console.print(
            Panel(
                metadata_content,
                title=f"[bold yellow] TRACK DETAILS [/bold yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
        )

        nav1 = questionary.select(
            "Navigation:",
            choices=[
                questionary.Choice(title="<- Go Back", value="back"),
                questionary.Choice(title="<- Return to Main Menu", value="main"),
            ],
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if nav1 is None or nav1 == 'back': 
            break
        elif nav1 == 'main':
            flag = 1
            break
            
    return flag