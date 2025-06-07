from app.royal_road_client import RoyalRoadAPI
from dataclasses import dataclass
import pytest


@dataclass
class FictionInfo:
    fic_id: int
    slug: str
    title: str
    chapter_url: str


@pytest.fixture
def pale_lights() -> FictionInfo:
    return FictionInfo(
        fic_id=65058,
        slug="pale-lights",
        title="Pale Lights",
        chapter_url="/fiction/65058/pale-lights/chapter/2335472/chapter-9",
    )


@pytest.fixture
def rr_client() -> RoyalRoadAPI:
    return RoyalRoadAPI()


def test_search_fiction__well_formed(rr_client, pale_lights):
    search_for = pale_lights.title
    sp = rr_client.search_fiction(search_for)
    assert len(sp.fiction_items) == 1, (
        f"Expected to find 1 fiction item when searching for {search_for} but found {len(sp.fiction_items)}"
    )

    fiction_item = sp.fiction_items[0]
    assert fiction_item.fic_id == pale_lights.fic_id
    assert fiction_item.slug == pale_lights.slug
    assert fiction_item.pretty_fic_title == pale_lights.title


# TODO: add more tests around the search feature
# 1. Fuzzy matching
# 2. No results
# 3. Many results


def test_get_fiction__hit(rr_client, pale_lights):
    fp = rr_client.get_fiction(pale_lights.fic_id)
    assert fp.title == pale_lights.title
    assert len(fp.chapters) > 1


# TODO: add more tests around the get fiction call
# 1. No match


def test_get_chapter__hit(rr_client, pale_lights):
    chapter_url = pale_lights.chapter_url

    ch = rr_client.get_chapter(chapter_url)
    assert len(ch.content) > 0
