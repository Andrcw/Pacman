import pygame

class Stats:

    def __init__(self):
        # Should start with game as inactive
        self.game_active = True
        self.game_pause = False
        self.game_over = False
        self.get_ready = True
        self.index = 0

    def ready(self):
        if self.index >= 20:
            self.index = 0
            self.get_ready = False
        else:
            self.index += .3


