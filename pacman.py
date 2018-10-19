import sys
import pygame
from maze import Maze
import game_functions as gf
from pm import PM
from ghosts import Red, Blue, Pink, Orange
from stats import Stats
from display import Display


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((630, 800))
    pygame.display.set_caption("PACMAN")

    stats = Stats()

    # Draw maze
    mazefile = 'maze.txt'
    maze = Maze(screen, mazefile)

    # Pacman
    pm = PM(screen, maze)

    # Ghosts
    red = Red(screen, maze)
    blue = Blue(screen, maze)
    pink = Pink(screen, maze)
    orange = Orange(screen, maze)

    display = Display(screen, pm)

    while True:

        if stats.game_active:
            gf.check_events(screen, pm, maze, red, blue, pink, orange, stats, display)

            gf.update_screen(screen, pm, maze, red, blue, pink, orange, stats, display)

            pygame.display.flip()

run_game()


