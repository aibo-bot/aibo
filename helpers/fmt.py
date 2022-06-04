import calendar
from io import StringIO
from html.parser import HTMLParser

import discord

from helpers import constants


def success_message(message: str) -> str:
    return f"{constants.EMOJIS.green_check} | {message}"

def error_message(message: str) -> str:
    return f"{constants.EMOJIS.red_cross} | {message}"

def warning_message(message: str) -> str:
    return f"{constants.EMOJIS.warning} | {message}"

def wrap_with_invis(text: str, num: int) -> str:
    chars = constants.INVIS_CHAR * num
    return chars + text + chars

def _format_date_dict(data: dict) -> str:
    if None in set(data.values()):
        return "N/A"
    return (
        f"{data['day']} {calendar.month_name[(data['month'] or 1)]} {data['year']}"
    )

def fmt_anime_embed(data: dict) -> discord.Embed:
    title = data["title"]["english"] or data["title"]["romaji"]
    description = data["description"]
    image = data["bannerImage"]
    cover = data["coverImage"]["large"]
    nsfw = data["isAdult"]

    url = data["siteUrl"]

    start_date = data["startDate"]
    end_date = data["endDate"]

    episodes = data["episodes"] or "Unknown"

    description = strip_html(description) if description is not None else "*No Description Found*"

    embed = discord.Embed(
        title=title,
        description=description,
        colour=discord.Colour.random(),
        url=url
    )
    embed.add_field(
        name="Dates",
        value=f"> **Start:** {_format_date_dict(start_date)}\n> **End:** {_format_date_dict(end_date)}"
    )
    embed.add_field(
        name="Episodes",
        value=f"> {episodes} episodes"
    )
    embed.add_field(
        name="NSFW",
        value=f"> {warning_message('Yes') if nsfw else success_message('No')}"
    )

    embed.set_thumbnail(url=cover)
    embed.set_image(url=image)
    return embed

def fmt_manga_embed(data: dict) -> discord.Embed:
    title = data["title"]["english"] or data["title"]["romaji"]
    description = data["description"]
    image = data["bannerImage"]
    cover = data["coverImage"]["large"]
    nsfw = data["isAdult"]

    url = data["siteUrl"]

    start_date = data["startDate"]
    end_date = data["endDate"]

    episodes = data["volumes"] or "Unknown"

    description = strip_html(description) if description is not None else "*No Description Found*"

    embed = discord.Embed(
        title=title,
        description=description,
        colour=discord.Colour.random(),
        url=url
    )
    embed.add_field(
        name="Dates",
        value=f"> **Start:** {_format_date_dict(start_date)}\n> **End:** {_format_date_dict(end_date)}"
    )
    embed.add_field(
        name="Volumes",
        value=f"> {episodes} volumes"
    )
    embed.add_field(
        name="NSFW",
        value=f"> {warning_message('Yes') if nsfw else success_message('No')}"
    )

    embed.set_thumbnail(url=cover)
    embed.set_image(url=image)
    return embed

class _StripHtmlParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.text = StringIO()
        super().__init__()

    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_html(string: str) -> str:
    parser = _StripHtmlParser()
    parser.feed(string)
    return parser.get_data()
    