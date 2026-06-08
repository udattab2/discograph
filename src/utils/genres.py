import sqlite3
import utils.albums as albums
from utils.helper import clear_screen, console
from utils.models import Genre
from rich.panel import Panel
import questionary

def gen_browse(ch0: str, flag: int, cur: sqlite3.Cursor) -> int:		
    while True:
        clear_screen()
        if flag == 1:
            break

        console.print(
            Panel.fit(
                "[bold cyan]GENRES[/bold cyan]\n"
                "[dim]Browse albums by selecting a musical genre[/dim]",
                border_style="cyan"
            )
        )

        cur.execute("SELECT id, name FROM genre")
        rows = cur.fetchall()
        genres = [Genre.from_row(r) for r in rows]

        # Build options dynamically
        choices: list[questionary.Choice] = []

        for gen in genres:
            choices.append(questionary.Choice(title=gen.name, value=str(gen.id)))
        
        choices.append(questionary.Choice(title="<- Go Back", value="back"))
        choices.append(questionary.Choice(title="<- Return to Main Menu", value="main"))

        ch4 = questionary.select(
            "Select a Genre:",
            choices=choices,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:green'),
            ])
        ).ask()

        if ch4 is None or ch4 == "back":
            break
        elif ch4 == "main":
            flag = 1
            break

        cur.execute("SELECT name FROM genre WHERE id=?", (ch4,))
        gr2 = cur.fetchone()
        
        flag = albums.alb_browse(ch0, gr2, ch4, flag, cur)
        
    return flag