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
        self.rect.x = 300
        self.rect.y = 230

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
            else:
                file = "g_red_left_1"
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

        self.ai(maze)
        self.dead_collide(pm, maze)

    def ai(self, maze):
        """Make the ghost move by itself"""
        """Making the ghost move out of the jail"""
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.stop_ball(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.avail) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
                print("ERROR: NO MOVES AVAILABLE")

            else:
                rand = random.choice(self.avail)
                self.move = rand

        # if gf.stop_ball(self, maze) is True and self.eat is True:
        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.avail:
                    self.move = "r"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.avail:
                    self.move = "l"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.avail:
                    self.move = "d"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.avail:
                    self.move = "u"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
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

    def dead_collide(self, pm, maze):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class Blue(Sprite):
    BLUE_SIZE = 30

    def __init__(self, screen, maze):
        super(Blue, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "g_blue_left_1", Blue.BLUE_SIZE, Blue.BLUE_SIZE)
        self.rect = self.image.rect

        # Starts the Blue ghost at this location
        self.rect.x = 250
        self.rect.y = 330

        self.maze = maze

        # Setting movement flags - Blue ghost starts moving left on game start
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
                    file = "g_blue_left_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "g_blue_right_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "g_blue_down_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "g_blue_up_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_up"
            else:
                file = "g_blue_left_1"
            self.image = ImageRect(screen, file, Blue.BLUE_SIZE, Blue.BLUE_SIZE)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        """For the dead ghosts"""
        if self.alive is False and self.eat is False:
            file = "evil_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, Blue.BLUE_SIZE, Blue.BLUE_SIZE)
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

        self.ai(maze)
        self.dead_collide(pm, maze)

    def ai(self, maze):
        """Make the ghost move by itself"""
        """Making the ghost move out of the jail"""
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.stop_ball(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.avail) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
                print("ERROR: NO MOVES AVAILABLE")

            else:
                rand = random.choice(self.avail)
                self.move = rand

        # if gf.stop_ball(self, maze) is True and self.eat is True:
        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.avail:
                    self.move = "r"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.avail:
                    self.move = "l"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.avail:
                    self.move = "d"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.avail:
                    self.move = "u"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
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

    def dead_collide(self, pm, maze):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class Pink(Sprite):
    PINK_SIZE = 30

    def __init__(self, screen, maze):
        super(Pink, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "g_pink_left_1", Pink.PINK_SIZE, Pink.PINK_SIZE)
        self.rect = self.image.rect

        # Starts the pink ghost at this location
        self.rect.x = 300
        self.rect.y = 330

        self.maze = maze

        # Setting movement flags - pink ghost starts moving left on game start
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
                    file = "g_pink_left_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "g_pink_right_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "g_pink_down_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "g_pink_up_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_up"
            else:
                file = "g_pink_left_1"
            self.image = ImageRect(screen, file, Pink.PINK_SIZE, Pink.PINK_SIZE)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        """For the dead ghosts"""
        if self.alive is False and self.eat is False:
            file = "evil_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, Pink.PINK_SIZE, Pink.PINK_SIZE)
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

        self.ai(maze)
        self.dead_collide(pm, maze)

    def ai(self, maze):
        """Make the ghost move by itself"""
        """Making the ghost move out of the jail"""
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.stop_ball(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.avail) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
                print("ERROR: NO MOVES AVAILABLE")

            else:
                rand = random.choice(self.avail)
                self.move = rand

        # if gf.stop_ball(self, maze) is True and self.eat is True:
        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.avail:
                    self.move = "r"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.avail:
                    self.move = "l"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.avail:
                    self.move = "d"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.avail:
                    self.move = "u"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
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

    def dead_collide(self, pm, maze):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class Orange(Sprite):
    ORANGE_SIZE = 30

    def __init__(self, screen, maze):
        super(Orange, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "g_orange_left_1", Orange.ORANGE_SIZE, Orange.ORANGE_SIZE)
        self.rect = self.image.rect

        # Starts the Orange ghost at this location
        self.rect.x = 350
        self.rect.y = 330

        self.maze = maze

        # Setting movement flags - Orange ghost starts moving left on game start
        self.direction = "l"
        self.move = "l"

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
                    file = "g_orange_left_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_left"
            elif self.move == "r":
                self.image.rect.x += self.speed
                if self.eat is False:
                    file = "g_orange_right_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_right"
            elif self.move == "d":
                self.image.rect.y += self.speed
                if self.eat is False:
                    file = "g_orange_down_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_down"
            elif self.move == "u":
                self.image.rect.y -= self.speed
                if self.eat is False:
                    file = "g_orange_up_" + str(math.floor(self.index))
                else:
                    file = "g_eyes_up"
            else:
                file = "g_orange_left_1"
            self.image = ImageRect(screen, file, Orange.ORANGE_SIZE, Orange.ORANGE_SIZE)
            self.image.rect = self.rect
            if self.index > 2.5:
                self.index = 1
            else:
                self.index += .1

        """For the dead ghosts"""
        if self.alive is False and self.eat is False:
            file = "evil_" + str(math.floor(self.dead_index))
            self.image = ImageRect(screen, file, Orange.ORANGE_SIZE, Orange.ORANGE_SIZE)
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

        self.ai(maze)
        self.dead_collide(pm, maze)

    def ai(self, maze):
        """Make the ghost move by itself"""
        """Making the ghost move out of the jail"""
        if self.move == "u" and self.rect == (300, 230, 30, 30):
            self.move = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.move = "u"

        if gf.stop_ball(self, maze) is True and self.eat is False:
            self.check_directions(maze)
            if len(self.avail) == 0:
                self.move = "l"
                self.move = "r"
                self.move = "u"
                self.move = "d"
                print("ERROR: NO MOVES AVAILABLE")

            else:
                rand = random.choice(self.avail)
                self.move = rand

        # if gf.stop_ball(self, maze) is True and self.eat is True:
        if self.eat is True:
            self.check_directions(maze)

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.avail:
                    self.move = "r"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.avail:
                    self.move = "l"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.avail:
                    self.move = "d"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.avail:
                    self.move = "u"
                elif gf.stop_ball(self, maze):
                    rand = random.choice(self.avail)
                    self.move = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.move = "d"
                elif self.rect.x < 300:
                    self.move = "r"
                elif self.rect.x > 300:
                    self.move = "l"
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

    def dead_collide(self, pm, maze):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pygame.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.eat = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.eat = False
                    self.alive = True


class Cherry(Sprite):
    CHERRY_SIZE = 30

    def __init__(self, screen):
        super(Cherry, self).__init__()
        self.screen = screen.get_rect()
        self.image = ImageRect(screen, "cherry", Cherry.CHERRY_SIZE, Cherry.CHERRY_SIZE)
        self.rect = self.image.rect

        # Starts the cherry at this location
        self.rect.x = 300
        self.rect.y = 390

    def blitme(self):
        self.image.blitme()

    def update(self, pm):
        self.collide(pm)

    def collide(self, pm):
        """Collision for the dead ghost"""
        if pygame.sprite.collide_rect(self, pm):
            self.rect.x = 800
            self.rect.y = 800
            pm.score += 200
            eat = pygame.mixer.Sound('sounds/eatfruit.wav')
            eat.play()
