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

        self.fic_id = int(href[2])
        self.slug = href[3]

        # Pretty Title
        h2 = soup.find_next("h2", {"class": "fiction-title"})
        assert h2 is not None, (
            f"When trying to parse FictionItem could not find h2 under {soup}"
        )
        self.pretty_fic_title = a.text

        # Book Cover
        img = a.find_next("img")
        assert img is not None, f"Could not find a <img> tag under in {img}"
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
        _fiction_items = fiction_list.find_next("div", {"class", "fiction-list-item"})

        self.fiction_items = [FictionItem(_fi) for _fi in _fiction_items]


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
        sp = SearchPage(soup)
        return sp

    # def get_fiction(self, fic_id: int):
    #    route = f"{self.base_url}/fiction/{fic_id}"

    #    resp = requests.get(
    #        route,
    #    )

    #    if not resp.ok:
    #        raise Exception(f"Something went wrong getting {route}")

    #    data = resp.content.decode("UTF-8")
