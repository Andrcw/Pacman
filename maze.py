import pygame
from imagerect import ImageRect

class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 10

    def __init__(self, screen, mazefile, brickfile, ballfile):
        self.screen = screen
        self.filename = mazefile

        # Load line image and get its rect and change the size to 20 x 20
        # self.image = pygame.image.load('images/square.png')
        # self.image = pygame.transform.scale(self.image, (20, 20))
        # self.rect = self.image.get_rect()
        # self.screen_rect = screen.get_rect()

        with open('maze.txt', 'r') as f:
            self.rows = f.readlines()

        # for bricks
        self.bricks = []
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.deltax = self.deltay = Maze.BRICK_SIZE

        # for balls
        self.balls = []
        self.ball = ImageRect(screen, ballfile, 10, 10)
        self.ball_dx = self.ball_dy = 10

        self.build()

    def __str__(self):
        return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == '*':
                    self.balls.append(pygame.Rect(ncol * self.ball_dx, nrow * dy, w, h))

    def blitme(self):
        # self.screen.blit(self.image, self.rect)
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)

        for rect in self.balls:
            self.screen.blit(self.ball.image, rect)
