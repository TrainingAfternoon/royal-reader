from app.royal_road_client import RoyalRoadAPI

from textual import on
from textual.app import App, ComposeResult
from textual.containers import (
    VerticalScroll,
)
from textual.widgets import (
    Footer,
    Header,
    Label,
    Input,
    ContentSwitcher,
    DataTable,
    Markdown,
    Button,
)


class State:
    def __init__(self):
        self.rr_api = RoyalRoadAPI()
        self.known_fictions: set[str] = set()


class RoyalReaderApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        # with Horizontal(id="buttons"):
        #    yield Button("Search", id="search")
        #    yield Button("Saved", id="saved")
        with ContentSwitcher(initial="search-fictions"):
            with VerticalScroll(id="search-fictions"):
                yield Label()  # spacing
                yield Label("Search:")
                yield Label()  # spacing
                yield Input(placeholder="Royal Road Title")
                yield Label()  # spacing
                yield DataTable(id="search-table")
            with VerticalScroll(id="view-fiction"):
                yield Label()  # spacing
                yield Markdown(id="title")
                yield Label()  # spacing
                yield Label()  # spacing
                yield Label("Chapters:")
                yield Label()  # spacing
                yield Label()  # spacing
                yield DataTable(id="chapter-table")
        yield Footer()

    @on(Input.Submitted)
    def action_search_title(self, event: Input.Submitted) -> None:
        table = self.query_one(DataTable)

        rows_to_add: list[tuple[str]] = []
        sp = self.state.rr_api.search_fiction(event.value)
        for fi in sp.fiction_items:
            if fi.pretty_fic_title not in self.state.known_fictions:
                self.state.known_fictions.add(fi.pretty_fic_title)
                rows_to_add.append((fi.pretty_fic_title,))

        table.add_rows(rows_to_add)

    @on(DataTable.CellSelected)
    def action_view_fiction(self, event: DataTable.CellSelected) -> None:
        self.query_one(ContentSwitcher).current = "view-fiction"
        # title = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id

    def on_mount(self) -> None:
        self.title = "Royal Reader"
        self.theme = "gruvbox"
        self.state = State()

        table = self.query_one(DataTable)
        table.add_columns(
            "Title",
        )
        # table.add_rows(
        #    [
        #        (title.ljust(35), year)
        #        for title, year in (
        #            ("Dune", 1965),
        #            ("Dune Messiah", 1969),
        #            ("Children of Dune", 1976),
        #            ("God Emperor of Dune", 1981),
        #            ("Heretics of Dune", 1984),
        #            ("Chapterhouse: Dune", 1985),
        #        )
        #    ]
        # )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "tokyo-night" if self.theme == "gruvbox" else "gruvbox"


if __name__ == "__main__":
    app = RoyalReaderApp()
    app.run()
