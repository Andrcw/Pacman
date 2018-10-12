import sys
import pygame


def update_screen(screen, pm, maze):
    screen.fill((0, 0, 0))
    maze.blitme()
    pm.blitme()
    pm.update(maze, screen)

    # Display everything
    pygame.display.flip()


def check_events(screen, pm, maze):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_LEFT:
                pm.direction = "l"
                if brick_collision(pm, maze) is False:
                    pm.move = "l"
            elif event.key == pygame.K_RIGHT:
                pm.direction = "r"
                if brick_collision(pm, maze) is False:
                    pm.move = "r"
            elif event.key == pygame.K_UP:
                pm.direction = "u"
                if brick_collision(pm, maze) is False:
                    pm.move = "u"
            elif event.key == pygame.K_DOWN:
                pm.direction = "d"
                if brick_collision(pm, maze) is False:
                    pm.move = "d"

    ball_pm_collision(pm, maze)


def brick_collision(pm, maze):
    """Check if there is a collision brick and ball, otherwise keep moving"""
    if pm.direction == "l":
        temp = pm.rect.move(-1, 0)
    elif pm.direction == "r":
        temp = pm.rect.move(1, 0)
    elif pm.direction == "u":
        temp = pm.rect.move(0, -1)
    elif pm.direction == "d":
        temp = pm.rect.move(0, 1)

    for brick in maze.bricks:
        if brick.colliderect(temp):
            return True

    return False


def stop_ball(pm, maze):
    """Check if there is a collision brick and ball, and stop the ball"""
    if pm.move == "l":
        temp = pm.rect.move(-1, 0)
    elif pm.move == "r":
        temp = pm.rect.move(1, 0)
    elif pm.move == "u":
        temp = pm.rect.move(0, -1)
    elif pm.move == "d":
        temp = pm.rect.move(0, 1)

    for brick in maze.bricks:
        if brick.colliderect(temp):
            return True

    return False


def ball_pm_collision(pm, maze):
    """Check if there's a collision with Pacman, and the ball"""
    for balls in maze.balls:
        if balls.colliderect(pm):
            maze.balls.remove(balls)
            # Need to add scoring system here
