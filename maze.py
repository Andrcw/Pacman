import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 10
    BALL_SIZE = 5
    # PAC_SIZE = 10

    def __init__(self, screen, mazefile):
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
        self.brick = ImageRect(screen, "square", Maze.BRICK_SIZE, Maze.BRICK_SIZE)
        # self.brick_x = brick_y = Maze.BRICK_SIZE

        # for balls
        self.balls = []
        self.ball = ImageRect(screen, "ball", 10, 10)

        # for the line (gate)
        self.lines = []
        self.line = ImageRect(screen, "line", 10, 10)

        # for power pill
        self.pills = []
        self.pill = ImageRect(screen, "pill", 10, 10)

        self.build()

    def __str__(self):
        return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(ncol * Maze.BRICK_SIZE, nrow * Maze.BRICK_SIZE, w, h))
                if col == '*':
                    self.balls.append(pygame.Rect(ncol * Maze.BRICK_SIZE, nrow * Maze.BRICK_SIZE, w, h))
                if col == '-':
                    self.lines.append(pygame.Rect(ncol * Maze.BRICK_SIZE, nrow * Maze.BRICK_SIZE, w, h))
                if col == '8':
                    self.pills.append(pygame.Rect(ncol * Maze.BRICK_SIZE, nrow * Maze.BRICK_SIZE, w, h))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.balls:
            self.screen.blit(self.ball.image, rect)
        for rect in self.lines:
            self.screen.blit(self.line.image, rect)
        for rect in self.pills:
            self.screen.blit(self.pill.image, rect)
