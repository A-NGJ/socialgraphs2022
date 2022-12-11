import re


def print_header(title: str):
    """Prints pretty header"""
    print("=" * 20 + f" {title} " + "=" * 20 + "\n")


def initials(text: str) -> str:
    """Get initials of given text input"""
    return re.sub(
        r"\W", "", "".join(token[0].upper() for token in text.strip().split())
    )


# pylint: disable=too-few-public-methods
class Color:
    """
    Contains aliases to colors in HEX format
    """

    BLUE = "#00d7fc"
    BLACK = "#000000"
    WHITE = "#ffffff"
