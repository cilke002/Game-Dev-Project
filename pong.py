import pygame
import sys
import random
import time
import math

# ---- SETTINGS ----
WIDTH, HEIGHT = 1020, 750
BLOCK_SIZE = 30
LINE_WIDTH = 4
FPS = 60
BALL_SPEED = 8

EASY_CPU_SPEED = 7
MEDIUM_CPU_SPEED = 11
HARD_CPU_SPEED = 14

CPU_REACTION_TIME = WIDTH - 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 200, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---- MENUS ----
def start_menu():
    font = pygame.font.Font(None, 50)
    title_text = font.render("PONG", True, WHITE)
    select_text = font.render("Select Mode", True, WHITE)
    one_player_text = font.render("1 Player", True, WHITE)
    two_player_text = font.render("2 Player", True, WHITE)

    one_player = one_player_text.get_rect(center=(WIDTH // 2, 400))
    two_player = two_player_text.get_rect(center=(WIDTH // 2, 450))

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 8))
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(one_player_text, one_player.topleft)
        screen.blit(two_player_text, two_player.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if one_player.collidepoint(event.pos): 
                    return "1 Player"
                elif two_player.collidepoint(event.pos): 
                    return "2 Player"

def one_player_menu():
    font = pygame.font.Font(None, 50)
    select_text = font.render("Select Difficulty", True, WHITE)
    easy_text = font.render("EASY", True, WHITE)
    medium_text = font.render("MEDIUM", True, WHITE)
    hard_text = font.render("HARD", True, WHITE)
    back_text = font.render("BACK", True, WHITE)

    easy_mode = easy_text.get_rect(center=(WIDTH // 2, 400))
    medium_mode = medium_text.get_rect(center=(WIDTH // 2, 450))
    hard_mode = hard_text.get_rect(center=(WIDTH // 2, 500))
    back_box = back_text.get_rect(center=(WIDTH // 8, 675))

    while True:
        screen.fill(BLACK)
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(easy_text, easy_mode.topleft)
        screen.blit(medium_text, medium_mode.topleft)
        screen.blit(hard_text, hard_mode.topleft)
        screen.blit(back_text, back_box.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_mode.collidepoint(event.pos): 
                    return "EASY"
                elif medium_mode.collidepoint(event.pos): 
                    return "MEDIUM"
                elif hard_mode.collidepoint(event.pos): 
                    return "HARD"
                elif back_box.collidepoint(event.pos): 
                    return "BACK"

def color_select():
    font = pygame.font.Font(None, 50)
    select_text = font.render("SELECT BACKGROUND COLOR", True, WHITE)
    black_text = font.render("BLACK", True, WHITE)
    blue_text = font.render("BLUE", True, LIGHT_BLUE)

    black_box = black_text.get_rect(center=(WIDTH // 2, 400))
    blue_box = blue_text.get_rect(center=(WIDTH // 2, 450))

    while True:
        screen.fill(BLACK)
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, 300))
        screen.blit(black_text, black_box.topleft)
        screen.blit(blue_text, blue_box.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if black_box.collidepoint(event.pos): 
                    return BLACK
                elif blue_box.collidepoint(event.pos): 
                    return LIGHT_BLUE

def end_game(winner, score):
    font = pygame.font.Font(None, 50)
    winner_text = font.render(f"PLAYER {winner} WINS", True, WHITE)
    score_text = font.render(f"{score[0]} - {score[1]}", True, WHITE)
    continue_text = font.render("Rematch?", True, WHITE)
    yes_text = font.render("YES", True, WHITE)
    no_text = font.render("NO", True, WHITE)

    yes_box = yes_text.get_rect(center=(WIDTH // 2 - 50, 550))
    no_box = no_text.get_rect(center=(WIDTH // 2 + 50, 550))

    while True:
        screen.fill(BLACK)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(yes_text, yes_box.topleft)
        screen.blit(no_text, no_box.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_box.collidepoint(event.pos): 
                    return True
                elif no_box.collidepoint(event.pos): 
                    return False

# ---- CLASSES ----
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE * 4)
        self.speed = BLOCK_SIZE // 2
        self.direction = 0

    @property
    def center(self):
        return self.rect.centery

    def move(self):
        self.rect.y += self.direction
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > HEIGHT: 
            self.rect.bottom = HEIGHT
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, player_scored):
        self.rect = pygame.Rect(WIDTH // 2 - BLOCK_SIZE // 2, HEIGHT // 2 - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE)
        self.dx = BALL_SPEED if player_scored == 0 else -BALL_SPEED
        self.dy = random.choice([-BALL_SPEED, BALL_SPEED])

    @property
    def center(self):
        return self.rect.centery

    @property
    def x(self):
        return self.rect.x

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def bounce(self):
        self.dy *= -1

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Game:
    def __init__(self, cpu_difficulty):
        self.p1 = Paddle(30, 300)
        self.p2 = Paddle(WIDTH - 60, 300)
        self.ball = Ball(1)
        self.score = [0, 0]
        self.cpu_difficulty = cpu_difficulty
        self.cpu_speed = {
            "EASY": EASY_CPU_SPEED,
            "MEDIUM": MEDIUM_CPU_SPEED,
            "HARD": HARD_CPU_SPEED,
            "None": None
        }[cpu_difficulty]
        self.paused = False
        self.serve_time = time.time() + 1  

    def draw(self, bg_color):
        screen.fill(bg_color)
        self.p1.draw()
        self.p2.draw()
        self.ball.draw()
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - LINE_WIDTH // 2, y, LINE_WIDTH, 10))
        font = pygame.font.Font(None, 100)
        s1 = font.render(str(self.score[0]), True, WHITE)
        s2 = font.render(str(self.score[1]), True, WHITE)
        screen.blit(s1, (WIDTH // 4 - s1.get_width() // 2, 75))
        screen.blit(s2, (WIDTH - WIDTH // 4 - s2.get_width() // 2, 75))
        pygame.display.flip()

    def hit_ball(self, paddle):
        angle = (self.ball.center - paddle.center) / (paddle.rect.height / 2)
        self.ball.dx *= -1
        self.ball.dy = BALL_SPEED * angle * 2
        diff = math.hypot(self.ball.dx, self.ball.dy) - math.hypot(BALL_SPEED, BALL_SPEED)

        if self.ball.dx > 0:
            self.ball.dx = self.ball.dx - diff
        else:
            self.ball.dx = self.ball.dx + diff

        if abs(self.ball.dx) < BALL_SPEED / 4:
            if self.ball.dx > 0:
                self.ball.dx = BALL_SPEED
            else:
                self.ball.dx = -BALL_SPEED
            new_dy = math.sqrt((math.hypot(BALL_SPEED, BALL_SPEED) ** 2) - ((BALL_SPEED / 4) ** 2))
            if self.ball.dy < 0:
                self.ball.dy = -new_dy
            else:
                self.ball.dy = new_dy

        if self.ball.dx > 0:
            self.ball.rect.left = paddle.rect.right + 1
        else:
            self.ball.rect.right = paddle.rect.left - 1
        
    def update(self):
        if time.time() < self.serve_time:  
            return

        self.ball.move()
        self.p1.move()
        self.p2.move()

        # Ball wall bounce
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.bounce()

        # Paddle hits ball
        if self.ball.rect.colliderect(self.p1.rect):
            self.hit_ball(self.p1)
        elif self.ball.rect.colliderect(self.p2.rect):
            self.hit_ball(self.p2)

        # Scoring
        if self.ball.rect.left > WIDTH:
            self.score[0] += 1
            self.ball = Ball(0)
            self.serve_time = time.time() + 1
        elif self.ball.rect.right < 0:
            self.score[1] += 1
            self.ball = Ball(1)
            self.serve_time = time.time() + 1

    def cpu_control(self):
        if self.cpu_difficulty != "None" and self.ball.dx > 0 and self.ball.x > CPU_REACTION_TIME:
            target_y = self.ball.center
            dist = target_y - self.p2.center
            if abs(dist) > self.cpu_speed:
                dist = self.cpu_speed if dist > 0 else -self.cpu_speed
            self.p2.rect.y += dist

    def run(self, bg_color):
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    if not self.paused:
                        if event.key == pygame.K_w:
                            self.p1.direction = -self.p1.speed
                        elif event.key == pygame.K_s:
                            self.p1.direction = self.p1.speed
                        if self.cpu_difficulty == "None":
                            if event.key == pygame.K_UP:
                                self.p2.direction = -self.p2.speed
                            elif event.key == pygame.K_DOWN:
                                self.p2.direction = self.p2.speed
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_w, pygame.K_s]:
                        self.p1.direction = 0
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.p2.direction = 0

            if not self.paused:
                if self.cpu_difficulty != "None":
                    self.cpu_control()
                self.update()
                self.draw(bg_color)

            if max(self.score) > 10:
                return self.score

# ---- MAIN LOOP ----
def main():
    while True:
        mode = start_menu()
        if mode == "1 Player":
            cpu = one_player_menu()
            if cpu == "BACK":
                continue
        else:
            cpu = "None"
        bg_color = color_select()
        playing = True
        while playing:
            score = Game(cpu).run(bg_color)
            winner = 1 if score[0] > score[1] else 2
            playing = end_game(winner, score)

if __name__ == "__main__":
    main()
