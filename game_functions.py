import sys
import pygame


def update_screen(screen, pm, maze, red, stats, display):
    screen.fill((0, 0, 0))
    maze.blitme()
    display.score_blit(screen, stats, pm)

    # Displays the blitme's
    pm.blitme()
    if stats.get_ready:
        red.blitme()
        stats.ready()

    if not stats.game_pause and not stats.game_over and not stats.get_ready:
        pm.update(maze, screen)
        red.blitme()
        red.update(maze, screen)

    # Display everything
    pygame.display.flip()


def check_events(screen, pm, maze, red, stats, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_LEFT:   # Idea: change to TRUE, and keypress change to FALSE so that it loops
                pm.direction_l = True
            elif event.key == pygame.K_RIGHT:
                pm.direction_r = True
            elif event.key == pygame.K_UP:
                pm.direction_u = True
            elif event.key == pygame.K_DOWN:
                pm.direction_d = True
            elif event.key == pygame.K_p:
                print(stats.game_over)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pm.direction_l = False
            elif event.key == pygame.K_RIGHT:
                pm.direction_r = False
            elif event.key == pygame.K_UP:
                pm.direction_u = False
            elif event.key == pygame.K_DOWN:
                pm.direction_d = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            display.button_clicks(pm, stats)

    ball_pm_collision(pm, maze)
    pill_pm_collision(pm, maze, red)
    pm.ghost_collision(red, stats, screen)
    check_movement(pm, maze)


def check_movement(pm, maze):
    """To check movement and repeat on keypress"""
    if pm.direction_l is True:
        pm.direction = "l"
        if brick_collision(pm, maze) is False:
            pm.move = "l"
    elif pm.direction_r is True:
        pm.direction = "r"
        if brick_collision(pm, maze) is False:
            pm.move = "r"
    elif pm.direction_u is True:
        pm.direction = "u"
        if brick_collision(pm, maze) is False:
            pm.move = "u"
    elif pm.direction_d is True:
        pm.direction = "d"
        if brick_collision(pm, maze) is False:
            pm.move = "d"


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


def pill_pm_collision(pm, maze, red):
    """Check if pacman eats the pill"""
    for pills in maze.pills:
        if pills.colliderect(pm):
            maze.pills.remove(pills)
            red.alive = False
            red.dead_timer = 1


def reset_locations(pm, red, stats):
    """Reset the locations of pacman and red ghost"""
    pm.rect.x = pm.screen.centerx - 10
    pm.rect.y = pm.screen.centery + 110
    pm.move = "l"

    red.rect.x = red.screen.centerx - 15
    red.rect.y = red.screen.centery - 120

    if stats.game_over is False:
        stats.get_ready = True