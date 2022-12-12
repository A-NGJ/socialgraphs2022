import re


DEFAULT_FIGSIZE = (10, 6)
LARGE_FIGSIZE = (16, 12)


def print_header(title: str):
    """Prints (according to author) pretty header"""
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

    DEEP_SKY_BLUE = "#00d7fc"
    BLACK = "#000000"
    WHITE = "#ffffff"
    TORCH_RED = "#ed132c"
    SEAL_BROWN = "#3C1000"
    SADDLE_BROWN = "#972900"
    SUNSET_ORANGE = "#F54D3D"
