import sys
import pygame
from maze import Maze


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("PACMAN")

    # Draw maze
    mazefile = 'maze.txt'
    brickfile = 'images/square.png'
    ballfile = 'images/ball.png'
    maze = Maze(screen, mazefile, brickfile, ballfile)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Screen color
        bg_color = (0, 0, 0)
        screen.fill(bg_color)

        # Blit the maze
        maze.blitme()

        # Display
        pygame.display.flip()
run_game()


