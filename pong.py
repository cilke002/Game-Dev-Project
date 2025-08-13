import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1020, 750
BLOCK_SIZE = 30
LINE_WIDTH = 4
FPS = 30
BALL_SPEED = BLOCK_SIZE // 2
EASY_CPU_REACTION_TIME = WIDTH - 150
MEDIUM_CPU_REACTION_TIME = WIDTH - 175
HARD_CPU_REACTION_TIME = WIDTH // 2

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
    """Displays the start menu and returns selected mode."""
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if one_player.collidepoint(event.pos):
                    return "1 Player"
                elif two_player.collidepoint(event.pos):
                    return "2 Player"

def one_player_menu():
    """Displays menu for singleplayer mode, and returns selected CPU difficulty"""
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_mode.collidepoint(event.pos):
                    return "EASY"
                elif medium_mode.collidepoint(event.pos):
                    return "MEDIUM"
                elif hard_mode.collidepoint(event.pos):
                    return "HARD"
                elif back_box.collidepoint(event.pos):
                    return "BACK"

def end_game(winner, score):
    """Displays the game over screen and returns True to play again, False to quit."""
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_box.collidepoint(event.pos):
                    return True
                elif no_box.collidepoint(event.pos):
                    return False

# GAME LOGIC
def spawn_ball():
    """Spawn ball on random location along center line."""
    max_y = HEIGHT // BLOCK_SIZE
    while True:
        ball_x = WIDTH // 2 - 15
        ball_y = random.randint(0, max_y - 1) * BLOCK_SIZE
        return (ball_x, ball_y)

def move_paddle(paddle, direction):
    """Move one player's paddle in desired direction."""
    if direction == 0:
        return
    elif direction > 0:
        front = 3
    else:
        front = 0

    head_x, head_y = paddle[front]
    new_y = head_y + direction 

    if new_y < 0 or new_y > HEIGHT - 1:
        return  # Don’t move if out of bounds

    new_head = (head_x, new_y)

    if direction < 0:
        paddle.insert(0, new_head)
        paddle.pop()
    else:
        paddle.insert(4, new_head)
        paddle.pop(0)

def cpu_move_paddle(paddle, paddle_direction, ball, ball_direction, reaction_time, ball_dest):
    """Move CPU paddle to hit ball once it's close enough for CPU to notice"""
    new_paddle_direction = paddle_direction
    paddle_y = list()
    for segment in paddle:
        paddle_y.append(segment[1])
    if ball_dest not in paddle_y and ball[0] > reaction_time:
        if ball_dest < paddle[0][1] and paddle_direction > 0:
            new_paddle_direction = paddle_direction * -1
        elif ball_dest > paddle[3][1] and paddle_direction < 0:
            new_paddle_direction = paddle_direction * -1
        if ball_direction[0] > 0:
            move_paddle(paddle, new_paddle_direction)

def check_collision(ball, paddle):
    """Check if ball hits paddle."""
    for segment in paddle:
        if abs(ball[0] - segment[0]) < BLOCK_SIZE and abs(ball[1] - segment[1]) < BLOCK_SIZE:
            return True
    return False

def calc_trajectory(ball, paddles, ball_direction):
    """Calculate the direction ball should move after paddle or wall collision."""
    if check_collision(ball, paddles[0]):
        ball_direction = (BALL_SPEED, ball_direction[1])
    elif check_collision(ball, paddles[1]):
        ball_direction = (-BALL_SPEED, ball_direction[1])
    elif ball[1] >= HEIGHT:
        ball_direction = (ball_direction[0], -BALL_SPEED)
    elif ball[1] <= 0:
        ball_direction = (ball_direction[0], BALL_SPEED)

    return ball_direction

def calc_ball_dest(ball, ball_direction):
    """Calculate where the ball will end up based on its trajectory at the center line."""
    if ball_direction[1] < 0:
        ball_y = ball[1] - (8 * BLOCK_SIZE)
        ball_y *= -1
    else:
        ball_y = ball[1] + (8 * BLOCK_SIZE)

    ball_dest = (((WIDTH // 2) - (2 * BLOCK_SIZE)) // BLOCK_SIZE) * abs(ball_direction[1]) + ball_y
    if ball_dest > HEIGHT:
        ball_dest = ball_dest - ((ball_dest - HEIGHT) * 2)
    elif ball_dest < 0:
        ball_dest = ball_dest * -1

    return ball_dest

def move_ball(ball, ball_direction):
    """Move the ball and return its new position."""
    ball_x, ball_y = ball
    ball_dx, ball_dy = ball_direction
    return (ball_x + ball_dx, ball_y + ball_dy)


def run_game(cpu):
    """Run one full game."""
    p1 = [(30, 300), (30, 330), (30, 360), (30, 390)]
    p2 = [(960, 300), (960, 330), (960, 360), (960, 390)]
    paddles = [p1, p2]
    d1 = 0
    d2 = 0
    paused = False
    running = True
    ball = spawn_ball()
    ball_direction = (-BALL_SPEED, BALL_SPEED)
    ball_dest = 0
    score = [0, 0]
    draw_game(paddles, ball, score)
    time.sleep(0.5)

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
                    if cpu == "None":
                        if event.key == pygame.K_UP:
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

        # CPU movement
        if cpu == "EASY":
            d2 = BLOCK_SIZE
            reaction_time = EASY_CPU_REACTION_TIME
        elif cpu == "MEDIUM":
            d2 = BLOCK_SIZE
            reaction_time = MEDIUM_CPU_REACTION_TIME
        elif cpu == "HARD":
            d2 = BLOCK_SIZE
            reaction_time = HARD_CPU_REACTION_TIME

        # Player movement
        new_ball_direction = calc_trajectory(ball, paddles, ball_direction)
        ball = move_ball(ball, new_ball_direction)
        move_paddle(p1, d1)

        if ball[0] == WIDTH // 2 and ball_direction[0] > 0:
            ball_dest = calc_ball_dest(ball, ball_direction)

        # pygame.draw.rect(screen, RED, (WIDTH - BLOCK_SIZE, ball_dest, BLOCK_SIZE, BLOCK_SIZE))
        # pygame.display.flip()
        
        if cpu == "None":
            move_paddle(p2, d2)
        else:
            cpu_move_paddle(p2, d2, ball, new_ball_direction, reaction_time, ball_dest)

        # Increment score and spawn new ball
        if ball[0] > WIDTH:
            score[0] += 1
            time.sleep(0.5)
            ball = spawn_ball()
        elif ball[0] < -BLOCK_SIZE:
            score[1] += 1
            time.sleep(0.5)
            ball = spawn_ball()

        # Draw game
        draw_game(paddles, ball, score)

        if score[0] > 10 or score[1] > 10:
            running = False
            return score
            
        ball_direction = new_ball_direction

def draw_game(paddles, ball, score):
    """TODO"""
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

    # Draw score
    font = pygame.font.Font(None, 100)
    score_1 = font.render(f"{score[0]}", True, WHITE)
    score_2 = font.render(f"{score[1]}", True, WHITE)
    screen.blit(score_1, (WIDTH // 4 - score_1.get_width() // 2, 75))
    screen.blit(score_2, (WIDTH - WIDTH // 4 - score_2.get_width() // 2, 75))

    pygame.display.flip()

# MAIN LOOP
def main():
    """Main driver function."""
    while True:
        mode = start_menu()
        if mode == "1 Player":
            cpu = one_player_menu()
            if cpu == "BACK":
                continue
        elif mode == "2 Player":
            cpu = "None"

        playing = True
        while playing:
            score = run_game(cpu)
            if score[0] > score[1]:
                winner = 1
            else:
                winner = 2
            playing = end_game(winner, score)

if __name__ == "__main__":
    main()
    