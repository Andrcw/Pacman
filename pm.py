import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect
import game_functions as gf
import math


class PM(Sprite):
    PAC_SIZE = 30

    def __init__(self, screen, maze):
        super(PM, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "p_left_2", PM.PAC_SIZE, PM.PAC_SIZE)
        self.rect = self.image.rect
        self.rect.x = self.screen.centerx - 10
        self.rect.y = self.screen.centery + 110
        self.maze = maze

        # Setting movement flags
        self.direction = "l"
        self.move = "l"

        # Speed
        self.speed = 5

        # Index for images
        self.index = 1

    def update(self, maze, screen):
        """Update position based on movement flags"""
        if gf.stop_ball(self, maze) is False:
            if self.move == "l":
                self.image.rect.x -= self.speed
                file = "p_left_" + str(math.floor(self.index))
            elif self.move == "r":
                self.image.rect.x += self.speed
                file = "p_right_" + str(math.floor(self.index))
            elif self.move == "d":
                self.image.rect.y += self.speed
                file = "p_down_" + str(math.floor(self.index))
            elif self.move == "u":
                self.image.rect.y -= self.speed
                file = "p_up_" + str(math.floor(self.index))
            self.image = ImageRect(screen, file, PM.PAC_SIZE, PM.PAC_SIZE)
            self.image.rect = self.rect
            if self.index >= 4:
                self.index = 1
            else:
                self.index += .3

    def blitme(self):
        self.image.blitme()
