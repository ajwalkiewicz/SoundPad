import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

_THIS_FOLDER: str = os.path.dirname(os.path.abspath(__file__))
PATH: str = os.path.join(_THIS_FOLDER, "data", "settings.json")
SYSTEM = sys.platform


class PublicConfig:
    DEFAULT_DIRECTORY: str = "samples"
    KEY_RANGE: str = "system_wide"
    FONT_TYPE: str = "Helvetica"
    FONT_SIZE: int = 10
    FONT: tuple[str, int] = (FONT_TYPE, FONT_SIZE)
    SHOW_SETTINGS: bool = False
    FADEOUT_LENGTH: int = 3000
    IS_ON_TOP: bool = True
    KEY_0_BEHAVIOR: str = "pause"

    @classmethod
    def load_from_json(cls, path: Path):
        try:
            with open(path, "r") as fd:
                settings: dict[str, Any] = json.load(fd)
            for option, value in settings.items():
                option = option.upper()
                logging.debug(f"{option}={value}")
                setattr(cls, option, value)

            cls.FONT = (cls.FONT_TYPE, cls.FONT_SIZE)

        except json.JSONDecodeError:
            logging.critical("Could not load settings, falling back to defaults")

        logging.info("Settings loaded")


class Image:
    open: str = "images/folder-2x.png"
    stop: str = "images/media-stop-2x.png"
    pause: str = "images/media-pause-2x.png"
    play: str = "images/media-play-2x.png"


class Text:
    help_message = """
Simple sound pad inspired by real professional sound pads. 
It allows to ascribe music file to the button and play it
by pressing the button or key on keyboard.
"""
    github: str = "https://github.com/ajwalkiewicz/SoundPad"


def open_settings() -> int:
    if SYSTEM == "win32":
        command = PATH
    else:
        command = f"xdg-open {PATH}"
    return os.system(command)


NUMBER_OF_BUTTONS = NUMBER_OF_CHANNELS = NUMBER_OF_SOUNDS = 9

# fmt: off
SYSTEM_WIDE_KEY_MAPPING: Dict[int, str] = {
    0: "0", 
    1: "7", 2: "8", 3: "9",
    4: "4", 5: "5", 6: "6",
    7: "1", 8: "2", 9: "3",
}

INSIDE_APP_KEY_MAPPING: Dict[int, str] = {
    0: "<KP_0>",
    1: "<KP_7>", 2: "<KP_8>", 3: "<KP_9>",
    4: "<KP_4>", 5: "<KP_5>", 6: "<KP_6>",
    7: "<KP_1>", 8: "<KP_2>", 9: "<KP_3>",
}
# fmt: on

KEY_MAPPING = (
    SYSTEM_WIDE_KEY_MAPPING
    if PublicConfig.KEY_RANGE == "system_wide"
    else INSIDE_APP_KEY_MAPPING
)

if SYSTEM == "win32":
    logging.info(f"Detected system: {sys.platform}. Use Windows configuration")
else:
    logging.info(f"Detected system: {sys.platform}. Use UNIX configuration")

PublicConfig.load_from_json(PATH)
