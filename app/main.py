from app.constants import TITLE

from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListView,
    ListItem,
)


class RoyalReaderApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label(TITLE)
        yield ListView(
            ListItem(Label("S Search")),
            ListItem(Label("D Directory")),
            ListItem(Label("C Configuration")),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Royal Reader"
        self.theme = "gruvbox"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "tokyo-night" if self.theme == "gruvbox" else "gruvbox"


if __name__ == "__main__":
    app = RoyalReaderApp()
    app.run()
