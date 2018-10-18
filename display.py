import pygame



class Display():
    def __init__(self, screen, pm):
        """Display score, and how many pacman left"""
        self.font = pygame.font.SysFont("monospace", 40)
        self.font_1 = pygame.font.SysFont("monospace", 25)

        self.yellow = (255, 255, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)

        self.score = self.font.render("SCORE", True, self.white)
        self.score_btn = self.score.get_rect()
        self.score_btn.centerx = screen.get_rect().centerx - 240
        self.score_btn.centery = screen.get_rect().centery + 330

        self.s = self.font.render(str(pm.score), True, self.yellow)
        self.s_btn = self.s.get_rect()
        self.s_btn.left = screen.get_rect().centerx - 180
        self.s_btn.centery = screen.get_rect().centery + 330

        self.lives = self.font.render("LIVES", True, self.white)
        self.lives_btn = self.lives.get_rect()
        self.lives_btn.centerx = screen.get_rect().centerx + 20
        self.lives_btn.centery = screen.get_rect().centery + 330

        self.li = self.font.render(str(pm.lives), True, self.yellow)
        self.li_btn = self.li.get_rect()
        self.li_btn.centerx = screen.get_rect().centerx + 80
        self.li_btn.centery = screen.get_rect().centery + 330

        self.ready = self.font.render("GET READY!", True, self.white)
        self.ready_btn = self.ready.get_rect()
        self.ready_btn.centerx = screen.get_rect().centerx
        self.ready_btn.centery = screen.get_rect().centery + 8

        self.play = self.font_1.render("PLAY AGAIN", True, self.yellow)
        self.play_btn = self.play.get_rect()
        self.play_btn.centerx = screen.get_rect().centerx
        self.play_btn.centery = screen.get_rect().centery - 73

        self.go = self.font.render("GAME OVER", True, self.red)
        self.go_btn = self.go.get_rect()
        self.go_btn.centerx = screen.get_rect().centerx
        self.go_btn.centery = screen.get_rect().centery + 8

    def score_blit(self, screen, stats, pm):
        # Update numbers for scores
        self.s = self.font.render(str(pm.score), True, self.yellow)
        self.li = self.font.render(str(pm.lives), True, self.yellow)

        # Blit the scoreboards
        screen.blit(self.score, self.score_btn)
        screen.blit(self.s, self.s_btn)
        screen.blit(self.lives, self.lives_btn)
        screen.blit(self.li, self.li_btn)

        if stats.get_ready and not stats.game_over:
            screen.blit(self.ready, self.ready_btn)

        """Displays game over screen, and high score"""
        if stats.game_over:
            # screen.fill((0, 0, 0))
            screen.blit(self.go, self.go_btn)
            screen.blit(self.play, self.play_btn)

    def button_clicks(self, pm, stats):
        play_clicked = self.play_btn.collidepoint(pygame.mouse.get_pos())
        if play_clicked and stats.game_over:
            print("play again")
            pm.lives = 3
            pm.score = 0
            stats.game_over = False


