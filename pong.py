import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1020, 750
BLOCK_SIZE = 30
LINE_WIDTH = 4
FPS = 30
BALL_SPEED = BLOCK_SIZE // 2

# Colors 
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
LIGHT_GREEN = (0, 255, 0)

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# MENUS
def start_menu():
    """TODO"""

def end_game():
    """TODO"""


# GAME LOGIC
def start_rally():
    """TODO"""

def spawn_ball():
    """TODO"""
    max_y = HEIGHT // BLOCK_SIZE
    while True:
        ball_x = WIDTH // 2 - 15
        ball_y = random.randint(0, max_y - 1) * BLOCK_SIZE
        return (ball_x, ball_y)

def move_paddle(paddle, direction):
    if direction == 0:
        return

    head_x, head_y = paddle[0]
    new_y = head_y + direction

    if new_y < 0 or new_y > HEIGHT - 1:
        return  # Don’t move if out of bounds

    new_head = (head_x, new_y)
    paddle.insert(0, new_head)
    paddle.pop()

def check_collision(ball, paddle):
    for segment in paddle:
        if abs(ball[0] - segment[0]) < BLOCK_SIZE and abs(ball[1] - segment[1]) < BLOCK_SIZE:
            return True
    return False

def calc_trajectory(ball, paddles, ball_direction):
    """TODO"""
    if check_collision(ball, paddles[0]):
        ball_direction = (BALL_SPEED, ball_direction[1])
    elif check_collision(ball, paddles[1]):
        ball_direction = (-BALL_SPEED, ball_direction[1])
    elif ball[1] >= HEIGHT:
        ball_direction = (ball_direction[0], -BALL_SPEED)
    elif ball[1] <= 0:
        ball_direction = (ball_direction[0], BALL_SPEED)

    return ball_direction

def move_ball(ball, ball_direction):
    """Move the ball and return its new position."""
    ball_x, ball_y = ball
    ball_dx, ball_dy = ball_direction
    return (ball_x + ball_dx, ball_y + ball_dy)


def run_game():
    """TODO"""
    p1 = [(30, 300), (30, 330), (30, 360), (30, 390)]
    p2 = [(960, 300), (960, 330), (960, 360), (960, 390)]
    paddles = [p1, p2]
    d1 = 0
    d2 = 0
    directions = [d1, d2]
    paused = False
    running = True
    ball = spawn_ball()
    ball_direction = (-BALL_SPEED, BALL_SPEED)
    score = [0, 0]
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_w:
                        d1 = -BLOCK_SIZE
                    elif event.key == pygame.K_s:
                        d1 = BLOCK_SIZE
                    elif event.key == pygame.K_UP:
                        d2 = -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN:
                        d2 = BLOCK_SIZE
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    d1 = 0
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    d2 = 0

        # Pause behavior
        if paused:
            font = pygame.font.Font(None, 60)
            screen.fill(BLACK)
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            continue

        # Movement
        new_ball_direction = calc_trajectory(ball, paddles, ball_direction)
        ball = move_ball(ball, new_ball_direction)
        move_paddle(p1, d1)
        move_paddle(p2, d2)

        # Increment score and spawn new ball
        if ball[0] > WIDTH:
            score[0] += 1
            ball = spawn_ball()
        elif ball[0] < 0:
            score[1] += 1
            ball = spawn_ball()

        if score[0] > 10 or score[1] > 10:
            pygame.quit()
            sys.exit()
        

        # Draw game
        draw_game(paddles, ball, score)
        ball_direction = new_ball_direction

def draw_game(paddles, ball, score):
    screen.fill(BLACK)

    # Draw each paddle segment as a block
    for paddle in paddles:
        for segment in paddle:
            pygame.draw.rect(screen, WHITE, (*segment, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(screen, WHITE, (*ball, BLOCK_SIZE, BLOCK_SIZE))
    # Draw dashed center line
    dash_height = 10
    gap = 10
    x = WIDTH // 2 - LINE_WIDTH // 2

    for y in range(0, HEIGHT, dash_height + gap):
        pygame.draw.rect(screen, WHITE, (x, y, LINE_WIDTH, dash_height))

    font = pygame.font.Font(None, 100)
    score_1 = font.render(f"{score[0]}", True, WHITE)
    score_2 = font.render(f"{score[1]}", True, WHITE)
    screen.blit(score_1, (WIDTH // 4 - score_1.get_width() // 2, 75))
    screen.blit(score_2, (WIDTH - WIDTH // 4 - score_2.get_width() // 2, 75))

    pygame.display.flip()

# MAIN LOOP
def main():
    """TODO"""
    # difficulty = start_menu()
    playing = True
    while playing:
        run_game()
        # playing = end_game(score, high_score)
    
if __name__ == "__main__":
    main()
    