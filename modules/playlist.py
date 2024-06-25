import logging
from collections import UserList
from typing import List, Union

from modules.audio import BaseSound, NoSound


class Playlist(UserList):
    """Class responsible for storing a playlist"""

    MAX_SOUNDS = 9

    def __init__(self, initlist=None, max_sounds: Union[int, None] = None) -> None:
        max_sounds = max_sounds or Playlist.MAX_SOUNDS

        if initlist is None:
            initlist: List[BaseSound] = [NoSound() for _ in range(max_sounds)]

        super().__init__(initlist=initlist)
        logging.debug(f"Initialized {self}")

    def get_paths(self) -> list[str]:
        return [sound.path if sound else "" for sound in self]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(initlist={self.data}, max_sounds={len(self)})"
