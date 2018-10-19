import sys
import pygame
from maze import Maze
import game_functions as gf
from pm import PM
from ghosts import Red, Blue, Pink, Orange, Cherry
from stats import Stats
from display import Display


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

    # Stats
    stats = Stats()

    # Ghosts
    red = Red(screen, maze)
    blue = Blue(screen, maze)
    pink = Pink(screen, maze)
    orange = Orange(screen, maze)
    cherry = Cherry(screen)

    display = Display(screen, pm)

    while True:
        if stats.game_active:
            gf.check_events(screen, pm, maze, red, blue, pink, orange, stats, display)

            gf.update_screen(screen, pm, maze, red, blue, pink, orange, cherry, stats, display)

            pygame.display.flip()

run_game()


