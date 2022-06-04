from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from helpers.deco import to_thread
from .common import add_corners

if TYPE_CHECKING:
    from ..models.account import Account


account_name_font = ImageFont.truetype("assets/fonts/inter/Inter-Bold.ttf", size=200)
account_about_me_fount = ImageFont.truetype("assets/fonts/inter/Inter-Medium.ttf", size=100)
stat_font = ImageFont.truetype("assets/fonts/inter/Inter-SemiBold.ttf", size=93)

@to_thread
def generate_account_image(
    name: str,
    account: Account,
    avatar: BytesIO
) -> BytesIO:
    template = Image.open("assets/images/accounts/accounts_template.png")
    avatar_img = Image.open(avatar) # type: ignore

    avatar_img = add_corners(avatar_img, 78)
    avatar_img = avatar_img.resize((899, 915))

    drawing = ImageDraw.Draw(template)
    drawing.text((1219, 330), name, fill=(255, 255, 255), font=account_name_font)
    drawing.text((1219, 615), account.description, fill=(158, 158, 158), font=account_about_me_fount)

    drawing.text((1219, 1010), "Level", fill=(255, 255, 255), font=stat_font)
    drawing.text((1725, 1010), "Experience", fill=(255, 255, 255), font=stat_font)
    drawing.text((2399, 1010), "Currency", fill=(255, 255, 255), font=stat_font)

    drawing.text((1219, 1124), str(account.level), fill=(158, 158, 158), font=stat_font)
    drawing.text((1725, 1124), f"{account.exp}/{account.max_exp}", fill=(158, 158, 158), font=stat_font)
    drawing.text((2399, 1124), str(account.currency), fill=(158, 158, 158), font=stat_font)

    box = Image.new("RGB", (2319, 90), color=(23, 34, 46))
    level_bar_shadow = add_corners(box, 20)

    multiplier = box.size[0] // account.max_exp
    x_size = (account.exp or 1) * multiplier

    bar_box = Image.new("RGB", (x_size, 90), color=(2, 132, 199))
    level_bar = add_corners(bar_box, 20)

    template.paste(level_bar_shadow, (1219, 841), level_bar_shadow)
    template.paste(level_bar, (1219, 841), level_bar)
    template.paste(avatar_img, (199, 292), avatar_img)

    buffer = BytesIO()
    template.save(buffer, format="png")

    buffer.seek(0)
    return buffer
    