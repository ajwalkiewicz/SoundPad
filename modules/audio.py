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

    def __init__(self, file: str, sound_id: int, isloop: int = 0, volume: float = 1.0):
        self.path: str = os.path.join(file)
        self.sound: Sound = pygame.mixer.Sound(self.path)
        self.id: int = sound_id
        self.isplaying: bool = True
        self.isloop: int = isloop
        self.length: float = self.sound.get_length()  # In seconds
        self.channel: Channel = pygame.mixer.Channel(self.id)
        self.set_volume(volume)
        logging.debug(f"INITIALIZE: {self}")

    def play(self):
        self.channel.play(self.sound, loops=self.isloop)
        self.isplaying = True
        logging.debug(f"PLAYED: {self}")

    def stop(self):
        self.channel.stop()
        logging.debug(f"STOPPED: {self}")

    def play_pause(self):
        if self.isplaying:
            self.channel.pause()
            self.isplaying = False
            logging.debug(f"PAUSED: {self}, isplaying: {self.isplaying}")
        else:
            self.channel.unpause()
            self.isplaying = True
            logging.debug(f"UNPAUSED: {self}, isplaying: {self.isplaying}")

    def fadeout(self, miliseconds: int):
        self.channel.fadeout(miliseconds)
        logging.debug(f"FADEOUT: {self}, value: {miliseconds}")

    def set_volume(self, new_volume: float):
        self.sound.set_volume(new_volume)
        self.channel.set_volume(1)  # volume equals: new_volume * 1
        logging.debug(f"VOLUME: {self} set to: {new_volume}")

    def __repr__(self) -> str:
        return f"SoundMusic(file='{self.path}', sound_id={self.id}, isloop={self.isloop} volume={self.sound.get_volume()})"

    # def __del__(self):
    #     """Report SoundMusic when objects are deleted while program is running."""
    #     logging.debug(f"DELETE: {self} from memory")


# TODO: get length
