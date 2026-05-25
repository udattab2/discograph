import sqlite3
import contextlib
import io
from typing import List, Optional

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static, Input, Button
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import ModalScreen
from textual.binding import Binding

import utils.addart as addart
from utils.models import Artist, Genre, Album, Track

class AddArtistModal(ModalScreen[str]):
    """Modal screen for adding a new artist with a clean overlay interface."""
    
    DEFAULT_CSS = """
    AddArtistModal {
        align: center middle;
        background: rgba(0, 0, 0, 0.65);
    }
    #dialog {
        width: 55;
        height: 11;
        border: thick $accent;
        background: $surface;
        padding: 1 2;
        border-title-align: center;
    }
    #title {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
        color: $accent;
    }
    #input {
        margin-bottom: 1;
        border: tall $primary-muted;
    }
    #buttons {
        layout: horizontal;
        height: 3;
        align: center middle;
    }
    Button {
        margin: 0 2;
        width: 15;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog") as v:
            v.border_title = "Add Artist"
            yield Label("Enter the name of the artist to import:", id="title")
            yield Input(placeholder="e.g. Coldplay, Taylor Swift...", id="input")
            with Horizontal(id="buttons"):
                yield Button("Cancel", id="cancel", variant="error")
                yield Button("Submit", id="submit", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss("")
        elif event.button.id == "submit":
            val = self.query_one("#input", Input).value
            self.dismiss(val)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class DiscographApp(App):
    """A premium, yazi-like three-column panelled TUI application for exploring discographies."""
    
    TITLE = "DISCOGRAPH"
    SUB_TITLE = "Modern Terminal Discography Explorer"
    
    BINDINGS = [
        Binding("f1", "switch_mode('artists')", "Artists Mode", show=True),
        Binding("f2", "switch_mode('genres')", "Genres Mode", show=True),
        Binding("f3", "toggle_search", "Search Tracks", show=True),
        Binding("f4", "add_artist", "Add Artist", show=True),
        Binding("escape", "clear_search", "Clear Search", show=False),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    DEFAULT_CSS = """
    Screen {
        background: $background;
    }
    
    #main-container {
        layout: horizontal;
        height: 1fr;
    }
    
    .pane {
        width: 33%;
        height: 100%;
        background: $background-lighten-1;
    }
    
    #left-pane {
        border: tall $primary-muted;
        border-title-align: left;
        layout: vertical;
    }
    
    #search-input {
        display: none;
        margin: 0 1 1 1;
        border: tall $accent;
    }
    
    #left-list {
        height: 1fr;
    }
    
    #middle-pane {
        border: tall $primary-muted;
        border-title-align: left;
    }
    
    #right-pane {
        border: tall $primary-muted;
        border-title-align: left;
        padding: 1 2;
    }
    
    #right-pane-content {
        height: auto;
    }
    
    ListView > ListItem {
        padding: 0 1;
        height: 3;
        content-align: left middle;
    }
    
    ListView > ListItem.--highlight {
        background: $accent-darken-1;
        color: $text;
        text-style: bold;
    }
    
    ListView:focus > ListItem.--highlight {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    #header {
        background: $accent-darken-2;
        color: $text;
        text-align: center;
        text-style: bold;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = sqlite3.connect("test2.db")
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        
        # Application state
        self.left_mode = "artists"  # "artists", "genres", "search"
        self.middle_view_mode = "albums"  # "albums", "tracks"
        self.selected_parent_id = None  # selected artist_id or genre_id
        self.selected_album_id = None
        self.selected_track_id = None

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Horizontal(id="main-container"):
            with Vertical(id="left-pane", classes="pane") as lp:
                lp.border_title = "ARTISTS"
                yield Input(placeholder="Type track name & Enter...", id="search-input")
                yield ListView(id="left-list")
                
            with Vertical(id="middle-pane", classes="pane") as mp:
                mp.border_title = "ALBUMS"
                yield ListView(id="middle-list")
                
            with ScrollableContainer(id="right-pane", classes="pane") as rp:
                rp.border_title = "PREVIEW"
                yield Static("[dim]Welcome to Discograph!\n\nUse Left/Right/Enter arrow keys to navigate between panels.\nPress F1/F2/F3/F4 to change modes and fetch data.[/dim]", id="right-pane-content")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_left_list()
        self.query_one("#left-list", ListView).focus()

    def refresh_left_list(self) -> None:
        """Refreshes the left column items based on current mode."""
        left_list = self.query_one("#left-list", ListView)
        left_list.clear()
        
        left_pane = self.query_one("#left-pane", Vertical)
        
        if self.left_mode == "artists":
            left_pane.border_title = "ARTISTS"
            self.cur.execute("SELECT id, name FROM artist ORDER BY name")
            rows = self.cur.fetchall()
            for r in rows:
                art = Artist.from_row(r)
                item = ListItem(Label(f"👤 {art.name}"), id=f"art_{art.id}")
                item.value = art.id
                left_list.append(item)
                
        elif self.left_mode == "genres":
            left_pane.border_title = "GENRES"
            self.cur.execute("SELECT id, name FROM genre ORDER BY name")
            rows = self.cur.fetchall()
            for r in rows:
                gen = Genre.from_row(r)
                item = ListItem(Label(f"🎸 {gen.name}"), id=f"gen_{gen.id}")
                item.value = gen.id
                left_list.append(item)

    def action_switch_mode(self, mode: str) -> None:
        """Switches browsing basis between Artists and Genres."""
        self.left_mode = mode
        self.query_one("#search-input", Input).display = False
        self.refresh_left_list()
        self.query_one("#left-list", ListView).focus()

    def action_toggle_search(self) -> None:
        """Toggles the inline search input widget."""
        search_input = self.query_one("#search-input", Input)
        if search_input.display:
            search_input.display = False
            self.query_one("#left-list", ListView).focus()
        else:
            search_input.display = True
            search_input.value = ""
            search_input.focus()

    def action_clear_search(self) -> None:
        """Clears current search results and goes back to Artists browsing."""
        self.action_switch_mode("artists")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Processes the track search input submissions."""
        if event.input.id == "search-input":
            query_str = event.value.strip()
            if not query_str:
                self.action_toggle_search()
                return
                
            self.left_mode = "search"
            self.query_one("#search-input", Input).display = False
            
            left_pane = self.query_one("#left-pane", Vertical)
            left_pane.border_title = f"SEARCH: '{query_str}'"
            
            left_list = self.query_one("#left-list", ListView)
            left_list.clear()
            
            self.cur.execute(
                "SELECT id, name, album_id, length, lyrics FROM track WHERE name LIKE ?",
                (f"%{query_str}%",)
            )
            rows = self.cur.fetchall()
            for r in rows:
                track = Track.from_row(r)
                item = ListItem(Label(f"🎵 {track.name}"), id=f"track_{track.id}")
                item.value = track.id
                left_list.append(item)
                
            left_list.focus()

    def action_add_artist(self) -> None:
        """Triggers the async background artist downloader modal workflow."""
        def handle_result(artist_name: str) -> None:
            if not artist_name or not artist_name.strip():
                return
            
            self.query_one("#right-pane-content", Static).update(
                f"[bold green]Adding '{artist_name}'...[/bold green]\n\n"
                "Connecting to MusicGraph API & downloading tracks asynchronously...\n"
                "Please wait, this will NOT block or freeze your terminal screen!"
            )
            self.query_one("#right-pane", ScrollableContainer).border_title = "DOWNLOADER"

            def worker_task():
                # Open thread-safe connection to perform background scrapings
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    with sqlite3.connect("test2.db") as thread_conn:
                        thread_cur = thread_conn.cursor()
                        addart.update(artist_name, thread_cur)
                        thread_conn.commit()

            def on_worker_finished(future):
                self.query_one("#right-pane-content", Static).update(
                    f"[bold green]Database Update Successful![/bold green]\n\n"
                    f"Discography data for '[cyan]{artist_name}[/cyan]' has been fetched and indexed successfully!\n"
                    "Press F1 to switch back and view the updated artist list."
                )
                self.query_one("#right-pane", ScrollableContainer).border_title = "STATUS"
                if self.left_mode == "artists":
                    self.refresh_left_list()

            self.run_worker(worker_task, exit_on_error=False, callback=on_worker_finished)

        self.push_screen(AddArtistModal(), handle_result)

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handles live item highlight changes, enabling instant yazi-like pane updates."""
        list_view = event.list_view
        item = event.item
        
        if not item:
            return
            
        if list_view.id == "left-list":
            self.on_left_highlighted(item.value)
        elif list_view.id == "middle-list":
            self.on_middle_highlighted(item.value)

    def on_left_highlighted(self, value: int) -> None:
        """Left panel highlight changed: updates Middle panel with albums/tracks preview."""
        self.selected_parent_id = value
        middle_list = self.query_one("#middle-list", ListView)
        middle_list.clear()
        
        middle_pane = self.query_one("#middle-pane", Vertical)
        
        if self.left_mode == "artists":
            middle_pane.border_title = "ALBUMS"
            self.middle_view_mode = "albums"
            
            self.cur.execute(
                "SELECT id, name, artist_id, year, trackcount FROM album WHERE artist_id=? ORDER BY album_no",
                (value, )
            )
            rows = self.cur.fetchall()
            for r in rows:
                alb = Album.from_row(r)
                year_str = f" ({alb.year})" if alb.year else ""
                tracks_str = f" [{alb.trackcount} tracks]" if alb.trackcount else ""
                item = ListItem(Label(f"💿 {alb.name}{year_str}{tracks_str}"), id=f"alb_{alb.id}")
                item.value = alb.id
                middle_list.append(item)
                
            self.query_one("#right-pane-content", Static).update(
                f"[bold cyan]Artist Profile Selected[/bold cyan]\n\n"
                f"Browse albums in the middle column.\n"
                f"Press [bold green]Right Arrow[/bold green] or [bold green]Enter[/bold green] to expand albums list."
            )
            
        elif self.left_mode == "genres":
            middle_pane.border_title = "ALBUMS"
            self.middle_view_mode = "albums"
            
            self.cur.execute(
                "SELECT DISTINCT album.id, album.name, album.artist_id, album.year, album.trackcount "
                "FROM album JOIN track ON album.id=track.album_id "
                "WHERE track.genre_id=? ORDER BY album.album_no",
                (value, )
            )
            rows = self.cur.fetchall()
            for r in rows:
                alb = Album.from_row(r)
                year_str = f" ({alb.year})" if alb.year else ""
                tracks_str = f" [{alb.trackcount} tracks]" if alb.trackcount else ""
                item = ListItem(Label(f"💿 {alb.name}{year_str}{tracks_str}"), id=f"alb_{alb.id}")
                item.value = alb.id
                middle_list.append(item)
                
            self.query_one("#right-pane-content", Static).update(
                f"[bold cyan]Genre Catalog Selected[/bold cyan]\n\n"
                f"Browse distinct albums containing tracks with this genre in the middle column.\n"
                f"Press [bold green]Right Arrow[/bold green] or [bold green]Enter[/bold green] to browse."
            )
            
        elif self.left_mode == "search":
            # Search mode: left panel lists tracks directly. 
            # We preview track details in middle pane, and lyrics in right pane.
            self.cur.execute(
                "SELECT name, length, album_id, genre_id, lyrics FROM track WHERE id=?",
                (value, )
            )
            track_row = self.cur.fetchone()
            if track_row:
                track = Track.from_row(track_row)
                
                # Fetch metadata
                self.cur.execute("SELECT name, release_year, trackcount, artist_id FROM album WHERE id=?", (track.album_id,))
                alb_row = self.cur.fetchone()
                album_name = alb_row['name'] if alb_row else "Unknown Album"
                artist_id = alb_row['artist_id'] if alb_row else None
                
                artist_name = "Unknown Artist"
                if artist_id:
                    self.cur.execute("SELECT name FROM artist WHERE id=?", (artist_id, ))
                    art_row = self.cur.fetchone()
                    artist_name = art_row['name'] if art_row else "Unknown Artist"
                
                middle_pane.border_title = "METADATA PREVIEW"
                middle_list.append(ListItem(Label(f"👤 Artist: {artist_name}")))
                middle_list.append(ListItem(Label(f"💿 Album: {album_name}")))
                middle_list.append(ListItem(Label(f"⏱ Length: {track.length}")))
                
                lyrics_text = track.lyrics if track.lyrics else "[dim]No lyrics available for this track.[/dim]"
                self.query_one("#right-pane-content", Static).update(
                    f"[bold yellow] TRACK LYRICS [/bold yellow]\n"
                    f"[bold cyan]Song:[/bold cyan] {track.name}\n\n"
                    f"{lyrics_text}"
                )

    def on_middle_highlighted(self, value: int) -> None:
        """Middle panel highlight changed: updates Right preview pane dynamically."""
        if not value:
            return
            
        if self.middle_view_mode == "albums":
            # We highlight an album: preview its tracklist in the Right column
            self.selected_album_id = value
            self.cur.execute("SELECT name, year, trackcount FROM album WHERE id=?", (value, ))
            alb = self.cur.fetchone()
            album_name = alb['name'] if alb else "Unknown Album"
            year = alb['year'] if alb else ""
            
            self.cur.execute("SELECT song_no, name, length FROM track WHERE album_id=? ORDER BY song_no", (value, ))
            rows = self.cur.fetchall()
            
            preview_text = f"[bold yellow] ALBUM TRACKLIST [/bold yellow]\n"
            preview_text += f"[bold cyan]{album_name}[/bold cyan] ({year})\n"
            preview_text += f"[dim]Tracks list:[/dim]\n\n"
            
            for r in rows:
                song_num = f"{r['song_no']}. " if r['song_no'] else ""
                preview_text += f"{song_num}{r['name']} ({r['length']})\n"
                
            self.query_one("#right-pane-content", Static).update(preview_text)
            
        elif self.middle_view_mode == "tracks":
            # We highlight a track: preview its lyrics in the Right column
            self.selected_track_id = value
            self.cur.execute("SELECT name, length, lyrics FROM track WHERE id=?", (value, ))
            track_row = self.cur.fetchone()
            if track_row:
                track = Track.from_row(track_row)
                lyrics_text = track.lyrics if track.lyrics else "[dim]No lyrics available for this track.[/dim]"
                
                self.query_one("#right-pane-content", Static).update(
                    f"[bold yellow] TRACK LYRICS [/bold yellow]\n"
                    f"[bold cyan]Song:[/bold cyan] {track.name} ({track.length})\n\n"
                    f"{lyrics_text}"
                )

    def show_tracks_for_selected_album(self) -> None:
        """Transitions the Middle column into listing tracks for the active album selection."""
        middle_list = self.query_one("#middle-list", ListView)
        active_item = middle_list.highlighted_child
        if not active_item:
            return
            
        album_id = active_item.value
        self.selected_album_id = album_id
        
        middle_list.clear()
        self.middle_view_mode = "tracks"
        
        self.cur.execute("SELECT name FROM album WHERE id=?", (album_id, ))
        alb = self.cur.fetchone()
        album_name = alb['name'] if alb else "Album"
        
        self.query_one("#middle-pane", Vertical).border_title = f"TRACKS: {album_name.upper()}"
        
        self.cur.execute(
            "SELECT id, name, lyrics, album_id, length, genre_id, song_no FROM track WHERE album_id=? ORDER BY song_no",
            (album_id, )
        )
        rows = self.cur.fetchall()
        for r in rows:
            track = Track.from_row(r)
            song_num = f"{track.song_no}. " if track.song_no else ""
            item = ListItem(Label(f"🎵 {song_num}{track.name} ({track.length})"), id=f"track_{track.id}")
            item.value = track.id
            middle_list.append(item)
            
        middle_list.focus()

    def show_albums_for_selected_parent(self) -> None:
        """Restores the Albums list in the Middle column for the active artist or genre selection."""
        if not self.selected_parent_id:
            return
            
        self.on_left_highlighted(self.selected_parent_id)
        
        middle_list = self.query_one("#middle-list", ListView)
        
        # Try to re-highlight the previously selected album
        if self.selected_album_id:
            for index, child in enumerate(middle_list.children):
                if child.value == self.selected_album_id:
                    middle_list.index = index
                    break
                    
        middle_list.focus()

    def on_key(self, event) -> None:
        """Implements pure h/j/k/l & arrow directional panels traversal navigation."""
        key = event.key
        focused = self.focused
        
        left_list = self.query_one("#left-list", ListView)
        middle_list = self.query_one("#middle-list", ListView)
        right_pane = self.query_one("#right-pane", ScrollableContainer)
        
        if key in ("right", "l"):
            if focused == left_list:
                if middle_list.children:
                    middle_list.focus()
            elif focused == middle_list:
                if self.middle_view_mode == "albums":
                    self.show_tracks_for_selected_album()
                else:
                    right_pane.focus()
                    
        elif key in ("left", "h", "backspace"):
            if focused == middle_list:
                if self.middle_view_mode == "tracks":
                    self.show_albums_for_selected_parent()
                else:
                    left_list.focus()
            elif focused == right_pane:
                middle_list.focus()

    def on_unmount(self) -> None:
        self.cur.close()
        self.conn.close()


def discograph():
    """Main wrapper function to instantiate and run the Discograph TUI App."""
    app = DiscographApp()
    app.run()

if __name__ == "__main__":
    discograph()
