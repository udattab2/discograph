from rich.console import Console

console = Console()

def clear_screen() -> None:
    """Clears the terminal screen using Rich's console.clear()."""
    console.clear()