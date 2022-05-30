import pygame
import os
import logging


class SoundMusic:
    """
    SoundMucic is an object that combines both
    pygame.miser.Sound and pygame.mixer.Channel
    to control music.
    """

    # channel_list = []
    id = 0

    def __init__(self, file, sound_id: int):
        self.path = os.path.join(file)
        self.sound = pygame.mixer.Sound(self.path)
        self.id = sound_id
        self.state = 1
        # SoundMusic.channel_list.append(self)
        self.channel = pygame.mixer.Channel(self.id)
        logging.debug(f"Initialize Sound object, path: {self.path}, id: {self.id}")

    def play(self):
        self.channel.play(self.sound)
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

# TODO:
# set volume
# get length
