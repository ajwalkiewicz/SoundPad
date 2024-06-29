from typing import List

import pygame
from modules.audio import BaseSound
from modules.playlist import Playlist
from modules import settings


class Player:
    """A controller class representing a player"""

    CONFIG = settings.PublicConfig

    def __init__(self, playlist: Playlist) -> None:
        self.playlist: List[BaseSound] = playlist
        self.fadeout_time = Player.CONFIG.FADEOUT_LENGTH

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

    def stop_all(self) -> None:
        pygame.mixer.stop()

    def play_pause_all(self) -> None:
        raise NotImplementedError()

    def fadeout_all(self, time: int | None = None) -> None:
        time = time or self.fadeout_time
        pygame.mixer.fadeout(time)
