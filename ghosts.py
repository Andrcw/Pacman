import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect
import game_functions as gf
import math
import random


class Red(Sprite):
    RED_SIZE = 30

    def __init__(self, screen, maze):
        super(Red, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "g_red_left_1", Red.RED_SIZE, Red.RED_SIZE)
        self.rect = self.image.rect

        # Starts the Red ghost at this location
        self.rect.x = self.screen.centerx - 15
        self.rect.y = self.screen.centery - 120

        self.maze = maze

        # Setting movement flags - Red ghost starts moving left on game start
        self.direction = "u"
        self.move = "u"

        # Speed
        self.speed = 5

        # Index for images
        self.index = 1

        # Get available directions
        self.avail = []

    def update(self, maze, screen):
        """Update position based on movement flags"""
        if gf.stop_ball(self, maze) is False:
            if self.move == "l":
                self.image.rect.x -= self.speed
                file = "g_red_left_" + str(math.floor(self.index))
            elif self.move == "r":
                self.image.rect.x += self.speed
                file = "g_red_right_" + str(math.floor(self.index))
            elif self.move == "d":
                self.image.rect.y += self.speed
                file = "g_red_down_" + str(math.floor(self.index))
            elif self.move == "u":
                self.image.rect.y -= self.speed
                file = "g_red_up_" + str(math.floor(self.index))
            self.image = ImageRect(screen, file, Red.RED_SIZE, Red.RED_SIZE)
            self.image.rect = self.rect
            if self.index >= 2:
                self.index = 1
            else:
                self.index += .3

        self.ai(maze, screen)

    def ai(self, maze, screen):
        """Make the ghost move by itself"""
        # Check while moving up
        # make sure if the ghost is at the center (start of the game) then it will move to the left
        if gf.stop_ball(self, maze) is True:
            self.check_directions(maze)

            if self.move == "u" and self.rect == (300, 230, 30, 30):
                self.move = "l"

            elif len(self.avail) == 0:
                self.move = "l"  # In case error, move left
                print("ERROR: NO MOVES AVAILABLE")

            else:
                rand = random.choice(self.avail)
                self.move = rand

    def check_directions(self, maze):
        # check which directions are available to move
        self.avail.clear()
        self.direction = "u"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "d":
                self.avail.append("u")

        self.direction = "d"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "u":
                self.avail.append("d")

        self.direction = "l"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "r":
                self.avail.append("l")

        self.direction = "r"
        if gf.brick_collision(self, maze) is False:
            if self.move is not "l":
                self.avail.append("r")

        # print(self.avail)

    def blitme(self):
        self.image.blitme()
