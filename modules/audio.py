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
        logging.debug(f"Initialize Sound object, path: {self.path}, id: {self.id}")

    def play(self):
        self.channel.play(self.sound, loops=self.is_looped)
        self.state = 1
        logging.debug(f"Sound played, id: {self.id}, path: {self.path}")

    def stop(self):
        self.channel.stop()
        logging.debug(f"Sound stopped, id: {self.id}, path: {self.path}")

    def play_pause(self):
        if self.state:
            self.channel.pause()
            self.state = 0
            logging.debug(
                f"Sound paused, state: {self.state}, id: {self.id}, path: {self.path}"
            )
        else:
            self.channel.unpause()
            self.state = 1
            logging.debug(
                f"Sound unpaused, state: {self.state}, id: {self.id}, path: {self.path}"
            )

    def fadeout(self, miliseconds: int):
        self.channel.fadeout(miliseconds)
        logging.debug(f"Sound fadeout, {miliseconds}, id: {self.id}, path: {self.path}")

    def set_volume(self, new_volume: float):
        self.sound.set_volume(new_volume)
        logging.debug(
            f"Sound volume set to: {new_volume}, id: {self.id}, path: {self.path}"
        )


# TODO:
# [x] set volume
# [ ] get length
