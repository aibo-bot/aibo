import sys
import logging

from colorama import init as init_colorama
from colorama import (
    Fore,
    Back,
    Style
)


init_colorama()

class ColourHandler(logging.Handler):
    def format(self, record: logging.LogRecord) -> str:
        level_name = record.levelname.upper()
        name = record.name
        message = record.getMessage()

        formatted = (
            f"{Fore.GREEN}{level_name}{Back.GREEN}{Style.RESET_ALL}:"
            f"{Fore.CYAN}{name}{Back.CYAN}{Style.RESET_ALL}:"
            f"{Fore.BLUE}{message}{Back.BLUE}{Style.RESET_ALL}"
        )

        return formatted

    def filter(self, record: logging.LogRecord) -> bool:
        return not ("pyboy" in record.name.lower())

    def emit(self, record: logging.LogRecord) -> None:
        formatted = self.format(record)
        print(formatted, file=sys.stdout)
