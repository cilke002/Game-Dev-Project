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

# ---- COLORS ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 200, 255)
DARK_BLUE = (0, 0, 75)
LIGHT_GREEN = (0, 200, 0)
DARK_GREEN = (0, 75, 0)
MENU_BG = (18, 20, 28)
BUTTON = (55, 55, 70)
BUTTON_HOVER = (95, 95, 125)
YELLOW = (255, 215, 0)

# Initialize game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---- HELPER FUNCTIONS ----
def draw_button(rect, text, font):
    mouse = pygame.mouse.get_pos()

    hover = rect.collidepoint(mouse)

    color = BUTTON_HOVER if hover else BUTTON

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)

    screen.blit(label, label_rect)


def draw_title(title):
    title_font = pygame.font.Font(None, 90)

    y = 90 + math.sin(time.time()*2)*5

    text = title_font.render(title, True, WHITE)

    screen.blit(text, (WIDTH//2-text.get_width()//2, y))


def draw_subtitle(text):

    font = pygame.font.Font(None, 42)

    label = font.render(text, True, (210,210,210))

    screen.blit(label,(WIDTH//2-label.get_width()//2,185))

# ---- MENUS ----
def start_menu():

    button_font = pygame.font.Font(None, 42)

    one_rect = pygame.Rect(0,0,260,55)
    two_rect = pygame.Rect(0,0,260,55)

    one_rect.center=(WIDTH//2,360)
    two_rect.center=(WIDTH//2,440)

    while True:

        screen.fill(MENU_BG)

        draw_title("PONG")

        draw_subtitle("Select Game Mode")

        draw_button(one_rect,"1 PLAYER",button_font)
        draw_button(two_rect,"2 PLAYER",button_font)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if one_rect.collidepoint(event.pos):
                    return "1 Player"

                if two_rect.collidepoint(event.pos):
                    return "2 Player"

def one_player_menu():

    button_font = pygame.font.Font(None,40)

    easy=pygame.Rect(0,0,260,55)
    medium=pygame.Rect(0,0,260,55)
    hard=pygame.Rect(0,0,260,55)

    easy.center=(WIDTH//2,340)
    medium.center=(WIDTH//2,420)
    hard.center=(WIDTH//2,500)

    back=pygame.Rect(20,HEIGHT-60,120,40)

    while True:

        screen.fill(MENU_BG)

        draw_title("PONG")

        draw_subtitle("Select Difficulty")

        draw_button(easy,"EASY",button_font)
        draw_button(medium,"MEDIUM",button_font)
        draw_button(hard,"HARD",button_font)

        pygame.draw.rect(screen,BUTTON,back,border_radius=8)
        pygame.draw.rect(screen,WHITE,back,2,border_radius=8)

        back_label=pygame.font.Font(None,32).render("BACK",True,WHITE)
        screen.blit(back_label,back_label.get_rect(center=back.center))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:

                if easy.collidepoint(event.pos):
                    return "EASY"

                if medium.collidepoint(event.pos):
                    return "MEDIUM"

                if hard.collidepoint(event.pos):
                    return "HARD"

                if back.collidepoint(event.pos):
                    return "BACK"

def color_select():

    button_font = pygame.font.Font(None, 40)

    color_options = [
        ("BLACK", BLACK),
        ("LIGHT BLUE", LIGHT_BLUE),
        ("DARK BLUE", DARK_BLUE),
        ("LIGHT GREEN", LIGHT_GREEN),
        ("DARK GREEN", DARK_GREEN)
    ]

    buttons = []

    start_y = 300
    spacing = 75

    for i in range(len(color_options)):
        rect = pygame.Rect(0, 0, 320, 55)
        rect.center = (WIDTH // 2, start_y + i * spacing)
        buttons.append(rect)

    while True:

        screen.fill(MENU_BG)

        draw_title("PONG")
        draw_subtitle("Select Background")

        mouse = pygame.mouse.get_pos()

        for i, (name, color) in enumerate(color_options):

            hover = buttons[i].collidepoint(mouse)

            fill = BUTTON_HOVER if hover else BUTTON

            pygame.draw.rect(screen, fill, buttons[i], border_radius=10)
            pygame.draw.rect(screen, WHITE, buttons[i], 2, border_radius=10)

            # Color preview square
            pygame.draw.rect(
                screen,
                color,
                (buttons[i].left + 15, buttons[i].centery - 12, 24, 24)
            )

            pygame.draw.rect(
                screen,
                WHITE,
                (buttons[i].left + 15, buttons[i].centery - 12, 24, 24),
                2
            )

            label = button_font.render(name, True, WHITE)
            label_rect = label.get_rect(center=buttons[i].center)

            screen.blit(label, label_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                for i, (_, color) in enumerate(color_options):

                    if buttons[i].collidepoint(event.pos):
                        return color

def end_game(winner, score):

    button_font = pygame.font.Font(None, 40)
    winner_font = pygame.font.Font(None, 55)
    score_font = pygame.font.Font(None, 50)

    rematch_rect = pygame.Rect(0, 0, 220, 55)
    quit_rect = pygame.Rect(0, 0, 220, 55)

    rematch_rect.center = (WIDTH // 2, 530)
    quit_rect.center = (WIDTH // 2, 610)

    while True:

        screen.fill(MENU_BG)

        # Animated title
        draw_title("GAME OVER")

        # Winner
        winner_text = winner_font.render(
            f"PLAYER {winner} WINS!",
            True,
            WHITE
        )

        winner_rect = winner_text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(winner_text, winner_rect)

        # Final Score
        score_text = score_font.render(
            f"{score[0]} - {score[1]}",
            True,
            WHITE
        )

        score_rect = score_text.get_rect(center=(WIDTH // 2, 260))
        screen.blit(score_text, score_rect)

        # Play Again
        play_again = pygame.font.Font(None, 42).render(
            "Play Again?",
            True,
            WHITE
        )

        play_rect = play_again.get_rect(center=(WIDTH // 2, 365))
        screen.blit(play_again, play_rect)

        # Buttons
        draw_button(rematch_rect, "REMATCH", button_font)
        draw_button(quit_rect, "QUIT", button_font)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if rematch_rect.collidepoint(event.pos):
                    return True

                elif quit_rect.collidepoint(event.pos):
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
                self.ball.dx = BALL_SPEED / 4
            else:
                self.ball.dx = -BALL_SPEED / 4
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
            else:
                font = pygame.font.Font(None, 60)
                pause_text = font.render("PAUSED", True, BLACK)
                screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                continue

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
