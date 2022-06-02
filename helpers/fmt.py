from helpers import constants


def success_message(message: str) -> str:
    return f"{constants.EMOJIS.green_check} | {message}"

def error_message(message: str) -> str:
    return f"{constants.EMOJIS.red_cross} | {message}"

def warning_message(message: str) -> str:
    return f":warning: | {message}"

def wrap_with_invis(text: str, num: int) -> str:
    chars = constants.INVIS_CHAR * num
    return chars + text + chars

