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

        # Setting movement flags - Pacman starts moving left as game starts
        self.direction = "l"
        self.move = "l"

        # Speed
        self.speed = 5
        self.tick_speed = 10
        self.timer = pygame.time.get_ticks()

        # Index for images
        self.index = 1
        self.dead_index = 1

        # Set movement flags as false
        self.direction_l = False
        self.direction_r = False
        self.direction_u = False
        self.direction_d = False

        # For the scores
        self.lives = 3
        self.score = 0

    def update(self, maze, screen):
        """Update position based on movement flags"""
        if gf.stop_ball(self, maze) is False and pygame.time.get_ticks() - self.timer >= self.tick_speed:
            self.timer = pygame.time.get_ticks()
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

        """For testing"""
        # print(self.rect.x)

    def ghost_collision(self, red, stats, screen):
        """Check if pacman collides with ghost, loses a life"""
        if pygame.sprite.collide_rect(self, red) and red.alive is True:
            stats.game_pause = True

        if stats.game_pause and red.alive is True:
            file = "p_dead_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, PM.PAC_SIZE, PM.PAC_SIZE)
            self.image.rect = self.rect
            if self.dead_index >= 6:
                self.dead_index = 1
                stats.game_pause = False

                # Decrease amount of lives left
                self.lives -= 1

                # Start again
                gf.reset_locations(self, red, stats)

            else:
                self.dead_index += .2

        if self.lives == 0:
            stats.game_over = True

    def blitme(self):
        self.image.blitme()
