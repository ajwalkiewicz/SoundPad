import pygame
import os
import logging

Sound: pygame.mixer.Sound
Channel: pygame.mixer.Channel


class SoundMusic:
    """
    SoundMucic is an object that combines both
    pygame.mixer.Sound and pygame.mixer.Channel
    to control music.
    """

    def __init__(self, file: str, sound_id: int):
        self.path: str = os.path.join(file)
        self.sound: Sound = pygame.mixer.Sound(self.path)
        self.id: int = sound_id
        self.state: int = 1
        self.is_looped: int = 0
        self.length: float = self.sound.get_length()  # In seconds
        self.channel: Channel = pygame.mixer.Channel(self.id)
        logging.debug(f"INITIALIZE: {self}")

    def play(self):
        self.channel.play(self.sound, loops=self.is_looped)
        self.state = 1
        logging.debug(f"PLAYED: {self}")

    def stop(self):
        self.channel.stop()
        logging.debug(f"STOPPED: {self}")

    def play_pause(self):
        if self.state:
            self.channel.pause()
            self.state = 0
            logging.debug(
                f"PAUSED: {self}, state: {self.state}"
            )
        else:
            self.channel.unpause()
            self.state = 1
            logging.debug(
                f"UNPAUSED: {self}, state: {self.state}"
            )

    def fadeout(self, miliseconds: int):
        self.channel.fadeout(miliseconds)
        logging.debug(f"FADEOUT: {self}, value: {miliseconds}")

    def set_volume(self, new_volume: float):
        self.sound.set_volume(new_volume)
        self.channel.set_volume(1)  # volume equals: new_volume * 1
        logging.debug(
            f"VOLUME: {self} set to: {new_volume}"
        )

    def __repr__(self) -> str:
        return f"SoundMusic(file='{self.path}', sound_id={self.id})"

    def __del__(self):
        """Report SoundMusic when objects are deleted while program is running."""
        logging.debug(f"DELETE: {self} from memory")


# TODO: get length
