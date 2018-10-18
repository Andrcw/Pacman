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
        self.tick_dead = 30
        self.tick_alive = 10
        self.tick_speed = self.tick_alive

        # Index for images
        self.index = 1
        self.dead_index = 1
        self.dead_timer = 1

        # Get available directions
        self.avail = []

        # Set state of pacman to start as alive
        self.alive = True
        self.eat = False

        # Ticks
        self.timer = pygame.time.get_ticks()

    def update(self, maze, screen, pm):
        """Update position based on movement flags"""
        if gf.stop_ball(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
            if self.move == "l":
                self.image.rect.x -= self.speed
                if self.eat is False:
                    file = "g_red_left_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "g_red_right_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "g_red_down_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "g_red_up_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_up"
            self.image = ImageRect(screen, file, Red.RED_SIZE, Red.RED_SIZE)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        """For the dead ghosts"""
        if self.alive is False and self.eat is False:
            file = "evil_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, Red.RED_SIZE, Red.RED_SIZE)
            self.image.rect = self.rect
            if self.dead_timer > 20:
                self.alive = True
            else:
                self.dead_timer += .05
                if self.dead_timer < 15:
                    if self.dead_index > 2.5:
                        self.dead_index = 1
                    else:
                        self.dead_index += .1
                else:
                    if self.dead_index > 3.5:
                        self.dead_index = 2
                    else:
                        self.dead_index += .1

        """Change speed of dead ghosts"""
        if self.alive is True:
            self.tick_speed = self.tick_alive
        elif self.alive is False:
            self.tick_speed = self.tick_dead

        self.ai(maze, screen)
        self.dead_collide(screen, pm, maze)

    def ai(self, maze, screen):
        """Make the ghost move by itself"""
        # Check while moving up
        # make sure if the ghost is at the center (start of the game) then it will move to the left
        if gf.stop_ball(self, maze) is True:   # Make this false later for self.eat
            self.check_directions(maze)

            if self.move == "u" and self.rect == (300, 230, 30, 30):
                self.move = "l"

            elif len(self.avail) == 0:
                self.move = "l"  # In case error, move left
                self.move = "r"
                self.move = "u"
                self.move = "d"
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

    def blitme(self):
        self.image.blitme()

    def dead_collide(self, screen, pm, maze):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            self.eat = True
