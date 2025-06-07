from bs4 import BeautifulSoup
import requests


class FictionItem:
    def __init__(self, soup: BeautifulSoup):
        # Attributes
        self.fic_id: int
        self.slug: str
        self.pretty_fic_title: str
        self.fic_cover_url: str

        # Fiction Id + URL Slug
        a = soup.find_next("a")
        assert a is not None, f"Could not find an <a> tag in {soup}"

        try:
            href = a["href"]
        except KeyError:
            raise Exception(
                f"When trying to parse FictionItem, could not find href under {a}"
            )

        components = href.split("/", 4)
        assert len(components) >= 4, (
            f"Expecting at least 4 components, only found {len(components)} in {components}"
        )

        self.fic_id = int(components[2])
        self.slug = components[3]

        # Pretty Title
        h2 = soup.find_next("h2", {"class": "fiction-title"})
        assert h2 is not None, (
            f"When trying to parse FictionItem could not find h2 under {soup}"
        )
        self.pretty_fic_title = h2.text.strip()

        # Book Cover
        img = a.img
        assert img is not None, (
            f"Expected to find <img> tag under {a} when parsing FictionItem"
        )
        try:
            img_src = img["src"]
        except KeyError:
            raise Exception(
                f"When trying to parse FictionItem, could not find src under {img}"
            )

        # NOTE: Fiction cover might have a time stamp on it, I think that's for
        # determing what cover to show when a fiction has multiple covers. If we
        # strip it off, it will just return the latest/active one from the site
        self.fic_cover_url = img_src.split("?")[0]


class SearchPage:
    def __init__(self, soup: BeautifulSoup):
        fiction_lists = soup.find_all("div", {"class": "fiction-list"})
        assert len(fiction_lists) == 1, "Should only find 1 fiction list when searching"

        fiction_list = fiction_lists[0]
        _fiction_items = fiction_list.find_all("div", {"class", "fiction-list-item"})

        self.fiction_items = [FictionItem(_fi) for _fi in _fiction_items]


class FictionPageChapters:
    def __init__(self, soup: BeautifulSoup):
        # Attrs
        self.title: str
        self.url: str

        # Title
        # TODO: error handling
        self.title = soup.a.text.strip()

        # URL
        # TODO: error handling
        self.url = soup.a["href"]
        assert self.url.startswith("/"), (
            "Expecting chapter urls to start with a '/' when parsing FictionPageChapters"
        )


class FictionPage:
    def __init__(self, soup: BeautifulSoup):
        # Attrs
        self.title: str
        self.cover_img_url: str
        self.chapters: list[FictionPageChapters]

        # Title + Cover Img
        fic_headers = soup.find_all("div", {"class": "fic-header"})
        assert len(fic_headers) == 1, (
            'Was only expecting to find one <div class="fic-header"> when parsing fiction page, but found multiple'
        )
        fic_header = fic_headers[0]

        # TODO: go back and add good error handling
        self.title = fic_header.find_all("h1")[0].text
        self.cover_img_url = fic_header.find_all("img")[0]["src"].split("?")[0]

        # Chapters
        chapter_tables = soup.find_all("table")
        assert len(chapter_tables) == 1, (
            f"Expecting to find 1 chapter table, instead found {len(chapter_tables)} when parsing fiction page"
        )
        chapter_table = chapter_tables[0]
        self.chapters = [
            FictionPageChapters(c)
            for c in chapter_table.find_all("td", {"class": None})
        ]


class Chapter:
    def __init__(self, soup: BeautifulSoup):
        # Attrs
        self.content: str

        # Content
        ccs = soup.find_all("div", {"class": "chapter-content"})
        assert len(ccs) == 1, (
            f"Expecting to find exactly 1 div with the chapter-content class, but found {len(ccs)}"
        )
        cc = ccs[0]
        self.content = cc.text


class RoyalRoadAPI:
    def __init__(self):
        self.base_url = "https://www.royalroad.com"

    def search_fiction(self, fic_name: str) -> SearchPage:
        route = f"{self.base_url}/fictions/search"

        resp = requests.get(
            route,
            params={
                "title": fic_name,
            },
        )

        if not resp.ok:
            raise Exception(f"Something went wrong searching for {fic_name}")

        data = resp.content.decode("UTF-8")
        soup = BeautifulSoup(data, "html.parser")
        return SearchPage(soup)

    def get_fiction(self, fic_id: int):
        route = f"{self.base_url}/fiction/{fic_id}"

        resp = requests.get(
            route,
        )

        if not resp.ok:
            raise Exception(f"Something went wrong getting {route}")

        data = resp.content.decode("UTF-8")
        soup = BeautifulSoup(data, "html.parser")
        return FictionPage(soup)

    def get_chapter(self, chapter_url: str) -> Chapter:
        route = f"{self.base_url}{chapter_url}"

        resp = requests.get(
            route,
        )

        if not resp.ok:
            raise Exception(f"Something went wrong getting {route}")

        data = resp.content.decode("UTF-8")
        soup = BeautifulSoup(data, "html.parser")
        return Chapter(soup)
