import logging
import os
from abc import ABC, abstractmethod

import pygame


class BaseSound(ABC):
    path = ""

    @property
    def isloop(self) -> int:
        return self.__isloop

    @isloop.setter
    def isloop(self, value) -> None:
        self.__isloop = value
        logging.debug(f"CHECKBOX new value: {value}")

    @abstractmethod
    def play(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def play_pause(self) -> None: ...

    @abstractmethod
    def fadeout(self, miliseconds: int) -> None: ...

    @abstractmethod
    def set_volume(self, new_volume: float) -> None: ...


class NoSound(BaseSound):
    """
    NoSound is a placeholder representing a track with
    no sound assigned.

    It implements all methods from BaseSound, but the do nothing
    except logging.
    """

    def play(self) -> None:
        logging.debug("EMPTY BUTTON: nothing to play")

    def stop(self) -> None:
        logging.debug("EMPTY BUTTON: nothing to stop")

    def play_pause(self) -> None:
        logging.debug("EMPTY BUTTON: nothing to play_pause")

    def fadeout(self, miliseconds: int) -> None:
        logging.debug("EMPTY BUTTON: nothing to fadeout")

    def set_volume(self, new_volume: float) -> None:
        logging.debug("EMPTY BUTTON: nothing to set volume")

    def __repr__(self) -> str:
        return type(self).__name__


class Sound(BaseSound):
    """
    Sound is an object that combines both
    pygame.mixer.Sound and pygame.mixer.Channel
    to control a single sound (song).
    """

    def __init__(
        self, file: str, sound_id: int, isloop: int = 0, volume: float = 1.0
    ) -> None:
        self.path: str = os.path.join(file)
        self.sound = pygame.mixer.Sound(self.path)
        self.id: int = sound_id
        self.isplaying: bool = True
        self.isloop: int = isloop
        self.length: float = self.sound.get_length()  # In seconds
        self.channel = pygame.mixer.Channel(self.id)
        self.set_volume(volume)
        logging.debug(f"INITIALIZE: {self}")

    def play(self) -> None:
        self.channel.play(self.sound, loops=self.isloop)
        self.isplaying = True
        logging.debug(f"PLAYED: {self}")

    def stop(self) -> None:
        self.channel.stop()
        logging.debug(f"STOPPED: {self}")

    def play_pause(self) -> None:
        if self.isplaying:
            self.channel.pause()
            self.isplaying = False
            logging.debug(f"PAUSED: {self}, isplaying: {self.isplaying}")
        else:
            self.channel.unpause()
            self.isplaying = True
            logging.debug(f"UNPAUSED: {self}, isplaying: {self.isplaying}")

    def fadeout(self, miliseconds: int) -> None:
        self.channel.fadeout(miliseconds)
        logging.debug(f"FADEOUT: {self}, value: {miliseconds}")

    def set_volume(self, new_volume: float) -> None:
        self.sound.set_volume(new_volume)
        self.channel.set_volume(1)  # volume equals: new_volume * 1
        logging.debug(f"VOLUME: {self} set to: {new_volume}")

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"file='{self.path}', "
            f"sound_id={self.id}, "
            f"isloop={self.isloop}, "
            f"volume={self.sound.get_volume()}"
            ")"
        )
