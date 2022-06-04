from typing import Tuple

from discord import ButtonStyle
from pyboy import WindowEvent


# emojis
class EMOJIS:
    green_check = "<:_:979855733086642240>"
    red_cross = "<:_:981247061632643132>"
    power_btn = "<:_:981623957826461806>"
    warning = "<:_:982243360758718536>"
    currency_coin = "<a:_:982248739974549504>"

EMBED_BG = 0x2F3136
INVIS_CHAR = "\u2800"

class _IconCls:
    def __init__(
        self,
        kwarg: str,
        value: str,
        *,
        disabled: bool = False
    ):
        self.kwarg = kwarg
        self.value = value
        self.disabled = disabled

def _icon(value: str, _type: str, *, disabled: bool = False):
    return _IconCls(_type, value, disabled=disabled)

# Gameboy
GAMEBOY_BUTTON_ICONS = {
    "blank": _icon(INVIS_CHAR, "label", disabled=True),
    "right": _icon("➡️", "emoji"),
    "left": _icon("⬅️", "emoji"),
    "up": _icon("⬆️", "emoji"),
    "down": _icon("⬇️", "emoji"),
    "a": _icon("🇦", "label"),
    "b": _icon("🇧", "label"),
    "select": _icon("Select", "label"),
    "power": _icon(EMOJIS.power_btn, "emoji")
}
GAMEBOY_BUTTON_STYLES = {
    "blank": ButtonStyle.gray,
    "right": ButtonStyle.blurple,
    "left": ButtonStyle.blurple,
    "up": ButtonStyle.blurple,
    "down": ButtonStyle.blurple,
    "a": ButtonStyle.blurple,
    "b": ButtonStyle.blurple,
    "select": ButtonStyle.green,
    "power": ButtonStyle.danger
}
GAMEBOY_BUTTON_BINDINGS: dict[str, None | Tuple[int, int]] = {
    "blank": None,
    "right": (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT),
    "left": (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT),
    "up": (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP),
    "down": (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN),
    "a": (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
    "b": (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
    "select": (WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT),
    "power": (WindowEvent.QUIT, WindowEvent.PASS)
}
ANILIST_ANIME_QUERY = """
query($search: String, $page: Int = 1, $per_page: Int = 10) {
    Page(page: $page, perPage: $per_page) {
        pageInfo {
            total
            currentPage
            lastPage
        }
        media(search: $search, type: ANIME, sort: POPULARITY_DESC) {
            title {
                romaji
                english
                native
            },
            description(asHtml: false)
            siteUrl
            bannerImage
            coverImage {
                large
            },
            startDate {
                year
                month
                day
            },
            endDate {
                year
                month
                day
            },
            episodes
            isAdult
        }
    }
}
"""
ANILIST_MANGA_QUERY = """
query($search: String, $page: Int = 1, $per_page: Int = 10) {
    Page(page: $page, perPage: $per_page) {
        pageInfo {
            total
            currentPage
            lastPage
        }
        media(search: $search, type: MANGA, sort: POPULARITY_DESC) {
            title {
                romaji
                english
                native
            },
            description(asHtml: false)
            siteUrl
            bannerImage
            coverImage {
                large
            },
            startDate {
                year
                month
                day
            },
            endDate {
                year
                month
                day
            },
            volumes
            isAdult
        }
    }
}
"""
