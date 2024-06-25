from typing import List

from modules.audio import BaseSound
from modules.playlist import Playlist


class Player:
    """A controller class representing a player"""

    def __init__(self, playlist: Playlist) -> None:
        self.playlist: List[BaseSound] = playlist

    def play(self, track: int) -> None:
        self.playlist[track].play()

    def stop(self, track: int) -> None:
        self.playlist[track].stop()

    def play_pause(self, track: int) -> None:
        self.playlist[track].play_pause()

    def fadeout(self, track: int, miliseconds: int) -> None:
        self.playlist[track].fadeout(miliseconds)

    def set_volume(self, track: int, volume: float) -> None:
        self.playlist[track].set_volume(volume)
