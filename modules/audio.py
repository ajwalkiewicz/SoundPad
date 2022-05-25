import pygame
import os
import logging

# import abc


# class AudioFile(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def play(self):
#         pass

#     @abc.abstractmethod
#     def stop(self):
#         pass

#     @classmethod
#     def __subclasshook__(cls, C):
#         if cls is AudioFile:
#             attrs = set(dir(C))
#             if set(cls.__abstractmethods__) <= attrs:
#                 return True
#         return NotImplemented


# class BackgroundMusic(AudioFile):
#     def __init__(self, file):
#         self.path = os.path.join(file)

#     def play(self):
#         pygame.mixer.music.load(self.path)
#         pygame.mixer.music.play(-1)

#     def stop(self):
#         pygame.mixer.music.stop()

#     def pause(self):
#         self.state = 1
#         if self.state:
#             pygame.mixer.music.pause()
#             self.state = 0
#         else:
#             pygame.mixer.music.unpause()


class SoundMusic:
    """
    SoundMucic is an object that combines both
    pygame.miser.Sound and pygame.mixer.Channel
    to control music.
    """

    channel_list = []
    id = 0

    def __init__(self, file, sound_id: int):
        self.path = os.path.join(file)
        self.sound = pygame.mixer.Sound(self.path)
        self.id = sound_id
        self.state = 1
        SoundMusic.channel_list.append(self)
        self.channel = pygame.mixer.Channel(self.id)
        logging.debug(f"Initialize Sound object, path: {self.path}, id: {self.id}")

    def play(self):
        self.channel.play(self.sound)
        self.state = 1
        logging.debug("Sound played")

    def stop(self):
        self.channel.stop()
        logging.debug(f"Sound stopped")

    def play_pause(self):
        if self.state:
            self.channel.pause()
            self.state = 0
            logging.debug(f"Sound paused, state: {self.state}")
        else:
            self.channel.unpause()
            self.state = 1
            logging.debug(f"Sound unpaused, state: {self.state}")

    def fadeout(self, miliseconds: int):
        self.channel.fadeout(miliseconds)
        logging.debug(f"Sound fadeout, {miliseconds}")
