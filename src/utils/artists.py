import sqlite3
import utils.addart as addart
import utils.albums as albums
from utils.helper import clear_screen, console
from utils.models import Artist
from rich.panel import Panel
import questionary

def art_browse(ch0: str, flag: int, cur: sqlite3.Cursor, conn: sqlite3.Connection) -> int:			
    while True:
        clear_screen()
        if flag == 1:
            break

        console.print(
            Panel.fit(
                "[bold cyan]ARTISTS[/bold cyan]\n"
                "[dim]Select an artist to view their albums, or add a new artist[/dim]",
                border_style="cyan"
            )
        )

        cur.execute("SELECT id, name FROM artist")
        rows = cur.fetchall()
        artists = [Artist.from_row(r) for r in rows]

        # Build options dynamically
        choices: list[questionary.Choice] = []

        for art in artists:
            choices.append(questionary.Choice(title=art.name, value=str(art.id)))
        
        choices.append(questionary.Choice(title="+ Add New Artist", value="add"))
        choices.append(questionary.Choice(title="<- Go Back", value="back"))
        choices.append(questionary.Choice(title="<- Return to Main Menu", value="main"))

        ch1 = questionary.select(
            "Select an Artist:",
            choices=choices,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if ch1 is None or ch1 == "back":
            break
        elif ch1 == "main":
            flag = 1
            break
        elif ch1 == "add":
            clear_screen()
            add1 = questionary.text("Enter Artist Name:").ask()
            if add1 and add1.strip():
                # Add a spinner while updating database
                with console.status(f"[bold green]Fetching info and updating database for '{add1}'...[/bold green]", spinner="dots"):
                    addart.update(add1, cur)
                conn.commit()
                questionary.press_any_key_to_continue("Artist added successfully! Press any key to continue...").ask()
            continue

        # Fetch artist name to pass to alb_browse
        cur.execute("SELECT name FROM artist WHERE id=?", (ch1,))
        nm2 = cur.fetchone()

        flag = albums.alb_browse(ch0, nm2, ch1, flag, cur)
        
    return flag
