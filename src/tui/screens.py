from textual.app import ComposeResult
from textual.widgets import Label, Input, Button
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen

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
