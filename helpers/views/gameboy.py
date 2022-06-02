from __future__ import annotations

from io import BytesIO
from typing import Tuple

import discord
from discord import ui

from pyboy import PyBoy
from PIL import Image

from helpers.fmt import (
    error_message,
    wrap_with_invis
)
from helpers.constants import EMBED_BG
from helpers.deco import to_thread
from helpers.constants import (
    GAMEBOY_BUTTON_ICONS,
    GAMEBOY_BUTTON_STYLES,
    GAMEBOY_BUTTON_BINDINGS,
    INVIS_CHAR
)


TICKS = 120
RENDER_EVERY = 3
HOLD_DURATION = 10

class GameboyButton(ui.Button):
    view: PyBoyView

    def __init__(self, name: str, row: int):
        icon = GAMEBOY_BUTTON_ICONS[name]
        style = GAMEBOY_BUTTON_STYLES[name]
        binding = GAMEBOY_BUTTON_BINDINGS[name]

        kwargs: dict[str, int | str | discord.ButtonStyle] = {
            "style": style,
            "row": row
        }

        kwargs[icon.kwarg] = icon.value
        kwargs["disabled"] = icon.disabled

        super().__init__(**kwargs)

        self.binding = binding
        self.binding_name = name

    async def callback(self, interaction: discord.Interaction) -> None:
        binding = self.binding
        if binding is None:
            await interaction.response.send_message(
                error_message("You can't click this button"),
                ephemeral=True
            )
            return

        await self.view.send_input(binding)

        if self.binding_name != "power":
            embed, file = await self.view.render_screen() # type: ignore
            await interaction.response.edit_message(
                embed=embed,
                attachments=[file],
                view=self.view
            )
        else:
            self.view.clear_items()
            self.view.stop()
            self.view.boy.stop(save=False)

            await interaction.response.edit_message(
                embed=None,
                attachments=[],
                view=None,
                content=f"Thanks for playing **`{self.view.boy.cartridge_title().title()}`** with us!"
            )

class RefreshButton(ui.Button):
    view: PyBoyView

    def __init__(self, row: int, size: int):
        label = wrap_with_invis("Refresh", size)
        style = discord.ButtonStyle.secondary
        super().__init__(
            label=label,
            style=style,
            row=row
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        embed, file = await self.view.render_screen()
        await interaction.response.edit_message(
            embed=embed,
            attachments=[file],
            view=self.view
        )

BLANK_BUTTON = lambda row: GameboyButton("blank", row)

BUTTONS = [
    BLANK_BUTTON(0), BLANK_BUTTON(0), GameboyButton("power", 0), BLANK_BUTTON(0), GameboyButton("select", 0), 
    BLANK_BUTTON(1), GameboyButton("up", 1), BLANK_BUTTON(1), BLANK_BUTTON(1), GameboyButton("a", 1),
    GameboyButton("left", 2), BLANK_BUTTON(2), GameboyButton("right", 2), GameboyButton("b", 2), BLANK_BUTTON(2),
    BLANK_BUTTON(3), GameboyButton("down", 3), BLANK_BUTTON(3), BLANK_BUTTON(3), BLANK_BUTTON(3),
    RefreshButton(4, 16)
]

class PyBoyView(ui.View):
    def __init__(
        self,
        rom: str,
        player: discord.User | discord.Member
    ):
        self.player = player
        self.rom = rom
        self.boy = self.load_rom(rom)
        self.frames: list[Image.Image] = []

        self.screen = self.boy.botsupport_manager().screen()

        super().__init__(timeout=200)

        for button in BUTTONS:
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.player.id:
            try:
                await interaction.response.send_message(
                    error_message("Sorry, you can't control this gameboy instance! Maybe try starting your own?"),
                    ephemeral=True
                )
            except Exception:
                pass
            
            return False
        
        return True

    @to_thread
    def tick(self, *, ticks: int = TICKS):
        for i in range(ticks):
            self.boy.tick()
            if not i % RENDER_EVERY:
                img = self.screen.screen_image()

                img = img.resize((256, 256), resample=Image.NEAREST) # type: ignore
                
                if img is None:
                    continue
                
                self.frames.append(img)

    async def send_input(self, event_pair: Tuple[int, int]):
        press, release = event_pair
        self.boy.send_input(press)
        await self.tick(ticks=HOLD_DURATION) # type: ignore
        self.boy.send_input(release)
        await self.tick(ticks=HOLD_DURATION) # type: ignore

    def load_rom(self, rom: str) -> PyBoy:
        boy = PyBoy(rom, window_type="headless")
        boy.set_emulation_speed(0)
        return boy

    async def render_screen(self, *, ticks: int = TICKS) -> Tuple[discord.Embed, discord.File]:
        await self.tick(ticks=ticks) # type: ignore

        buffer = BytesIO()
        first_frame = self.frames.pop(0)
        first_frame.save(buffer, format="gif", save_all=True, append_images=self.frames)
        
        buffer.seek(0)
        attachment = discord.File(buffer, filename="frames.gif")
        
        embed = discord.Embed(
            colour=EMBED_BG,
            title=str(self.boy.cartridge_title()).title()
        )
        embed.set_image(url="attachment://frames.gif")

        self.frames.clear()

        return (embed, attachment)
