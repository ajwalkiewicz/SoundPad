import logging
from collections import UserList

from modules.audio import NoSound, Sound
from modules import settings


class Playlist(UserList):
    """Class responsible for storing a playlist"""

    def __init__(
        self, initlist: list[Sound | NoSound] = None, max_sounds: None | int = None
    ) -> None:
        max_sounds = max_sounds or settings.NUMBER_OF_SOUNDS

        if initlist is None:
            initlist: list[NoSound] = [NoSound() for _ in range(max_sounds)]

        super().__init__(initlist=initlist)
        logging.debug(f"Initialized {self}")

    def get_paths(self) -> list[str]:
        return [sound.path for sound in self]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(initlist={self.data}, max_sounds={len(self)})"
