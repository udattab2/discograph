from tui.app import DiscographApp

def discograph() -> None:
    """Main wrapper function to instantiate and run the Discograph TUI App."""
    app = DiscographApp()
    app.run()

if __name__ == "__main__":
    discograph()
