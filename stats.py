import pygame

class Stats:

    def __init__(self):
        # Should start with game as inactive
        self.game_active = True
        self.game_pause = False
        self.game_over = False
        self.get_ready = True

        self.timer = pygame.time.get_ticks()

