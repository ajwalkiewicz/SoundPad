import pygame
import os
import abc


class AudioFile(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AudioFile:
            attrs = set(dir(C))
            if set(cls.__abstractmethods__) <= attrs:
                return True
        return NotImplemented


class BackgroundMusic(AudioFile):
    def __init__(self, file):
        self.path = os.path.join(file)

    def play(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        self.state = 1
        if self.state:
            pygame.mixer.music.pause()
            self.state = 0
        else:
            pygame.mixer.music.unpause()


class SoundMusic(AudioFile):
    def __init__(self, file):
        self.path = os.path.join(file)
        self.sound = pygame.mixer.Sound(self.path)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()
