import sys
import pygame


def update_screen(screen, pm, maze, red, stats):
    screen.fill((0, 0, 0))
    maze.blitme()

    # Displays the blitme's
    pm.blitme()
    if stats.get_ready:
        red.blitme()
    score(screen, pm, stats)

    if stats.get_ready:
        get_ready(stats)

    if not stats.game_pause and not stats.game_over and not stats.get_ready:
        pm.update(maze, screen)
        red.blitme()
        red.update(maze, screen)

    # Display everything
    pygame.display.flip()


def check_events(screen, pm, maze, red, stats):
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
                red.alive = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pm.direction_l = False
            elif event.key == pygame.K_RIGHT:
                pm.direction_r = False
            elif event.key == pygame.K_UP:
                pm.direction_u = False
            elif event.key == pygame.K_DOWN:
                pm.direction_d = False

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
    pm.rect.y = pm.screen.centery - 10
    pm.move = "l"
    red.rect.x = red.screen.centerx - 15
    red.rect.y = red.screen.centery - 120

    stats.get_ready = True


def score(screen, pm, stats):
    """Display score, and how many pacman left"""
    font = pygame.font.SysFont("monospace", 40)
    yellow = (255, 255, 0)
    white = (255, 255, 255)

    score = font.render("SCORE", True, white)
    score_btn = score.get_rect()
    score_btn.centerx = screen.get_rect().centerx - 240
    score_btn.centery = screen.get_rect().centery + 330

    s = font.render(str(pm.score), True, yellow)
    s_btn = s.get_rect()
    s_btn.left = screen.get_rect().centerx - 180
    s_btn.centery = screen.get_rect().centery + 330

    lives = font.render("LIVES", True, white)
    lives_btn = lives.get_rect()
    lives_btn.centerx = screen.get_rect().centerx + 20
    lives_btn.centery = screen.get_rect().centery + 330

    l = font.render(str(pm.lives), True, yellow)
    l_btn = l.get_rect()
    l_btn.centerx = screen.get_rect().centerx + 80
    l_btn.centery = screen.get_rect().centery + 330

    ready = font.render("GET READY!", True, white)
    ready_btn = ready.get_rect()
    ready_btn.centerx = screen.get_rect().centerx
    ready_btn.centery = screen.get_rect().centery + 8

    # Blit the scoreboards
    screen.blit(score, score_btn)
    screen.blit(s, s_btn)
    screen.blit(lives, lives_btn)
    screen.blit(l, l_btn)

    if stats.get_ready:
        screen.blit(ready, ready_btn)


def get_ready(stats):
    if stats.get_ready:
        print(pygame.time.get_ticks() - stats.timer)
        if pygame.time.get_ticks() - stats.timer > 2000:
            stats.get_ready = False
            stats.timer = pygame.time.get_ticks()
