import sys
import pygame
from maze import Maze
import game_functions as gf
from pm import PM


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((630, 800))
    pygame.display.set_caption("PACMAN")

    # Draw maze
    mazefile = 'maze.txt'

    maze = Maze(screen, mazefile)

    # Pacman
    pm = PM(screen, maze)

    while True:
        gf.check_events(screen, pm, maze)

        gf.update_screen(screen, pm, maze)

        # Display
        pygame.display.flip()

run_game()


