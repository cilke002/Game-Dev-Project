import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1020, 750
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
MENU_BG = (18,20,28)
BUTTON = (55,55,70)
BUTTON_HOVER = (90,90,120)

# Screen and clock
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

    button_font = pygame.font.Font(None, 40)

    easy_rect = pygame.Rect(0, 0, 280, 55)
    medium_rect = pygame.Rect(0, 0, 280, 55)
    hard_rect = pygame.Rect(0, 0, 280, 55)

    easy_rect.center = (WIDTH // 2, 340)
    medium_rect.center = (WIDTH // 2, 420)
    hard_rect.center = (WIDTH // 2, 500)

    while True:

        screen.fill(MENU_BG)

        draw_title("SNAKE GAME")
        draw_subtitle("Select Difficulty")

        # Easy
        pygame.draw.rect(
            screen,
            BUTTON_HOVER if easy_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON,
            easy_rect,
            border_radius=10
        )
        pygame.draw.rect(screen, GREEN, easy_rect, 2, border_radius=10)

        easy_label = button_font.render("EASY", True, WHITE)
        screen.blit(easy_label, easy_label.get_rect(center=easy_rect.center))

        # Medium
        pygame.draw.rect(
            screen,
            BUTTON_HOVER if medium_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON,
            medium_rect,
            border_radius=10
        )
        pygame.draw.rect(screen, BLUE, medium_rect, 2, border_radius=10)

        medium_label = button_font.render("MEDIUM", True, WHITE)
        screen.blit(medium_label, medium_label.get_rect(center=medium_rect.center))

        # Hard
        pygame.draw.rect(
            screen,
            BUTTON_HOVER if hard_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON,
            hard_rect,
            border_radius=10
        )
        pygame.draw.rect(screen, RED, hard_rect, 2, border_radius=10)

        hard_label = button_font.render("HARD", True, WHITE)
        screen.blit(hard_label, hard_label.get_rect(center=hard_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if easy_rect.collidepoint(event.pos):
                    return "EASY"

                elif medium_rect.collidepoint(event.pos):
                    return "MEDIUM"

                elif hard_rect.collidepoint(event.pos):
                    return "HARD"

def game_over_menu(score, high_score):

    button_font = pygame.font.Font(None, 40)
    label_font = pygame.font.Font(None, 42)
    big_font = pygame.font.Font(None, 80)

    rematch_rect = pygame.Rect(0, 0, 240, 55)
    quit_rect = pygame.Rect(0, 0, 240, 55)

    rematch_rect.center = (WIDTH // 2, 560)
    quit_rect.center = (WIDTH // 2, 640)

    while True:

        screen.fill(MENU_BG)

        # Animated title
        draw_title("GAME OVER")

        # FINAL SCORE label
        final_label = label_font.render(
            "FINAL SCORE",
            True,
            WHITE
        )

        final_rect = final_label.get_rect(center=(WIDTH // 2, 185))
        screen.blit(final_label, final_rect)

        # Large score
        score_text = big_font.render(
            str(score),
            True,
            GREEN
        )

        score_rect = score_text.get_rect(center=(WIDTH // 2, 255))
        screen.blit(score_text, score_rect)

        # HIGH SCORE label
        high_label = label_font.render(
            "HIGH SCORE",
            True,
            WHITE
        )

        high_rect = high_label.get_rect(center=(WIDTH // 2, 340))
        screen.blit(high_label, high_rect)

        # High score value
        if score > high_score:

            high_score_text = big_font.render(
                str(score),
                True,
                YELLOW
            )

            new_record = pygame.font.Font(None, 36).render(
                "★ NEW HIGH SCORE! ★",
                True,
                YELLOW
            )

            record_rect = new_record.get_rect(center=(WIDTH // 2, 470))
            screen.blit(new_record, record_rect)

        else:

            high_score_text = big_font.render(
                str(high_score),
                True,
                LIGHT_BLUE
            )

        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, 405))
        screen.blit(high_score_text, high_score_rect)

        # Play Again text
        play_again = label_font.render(
            "Play Again?",
            True,
            WHITE
        )

        play_rect = play_again.get_rect(center=(WIDTH // 2, 500))
        screen.blit(play_again, play_rect)

        # Buttons
        draw_button(rematch_rect, "YES", button_font)
        draw_button(quit_rect, "NO", button_font)

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

# GAME LOGIC
def spawn_food(snake):
    """Generates a food position not overlapping the snake."""
    max_x = WIDTH // BLOCK_SIZE
    max_y = HEIGHT // BLOCK_SIZE
    while True:
        food_x = random.randint(0, max_x - 1) * BLOCK_SIZE
        food_y = random.randint(0, max_y - 1) * BLOCK_SIZE
        if (food_x, food_y) not in snake:
            return (food_x, food_y)

def move_snake(snake, direction):
    """Returns new snake after moving."""
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.insert(0, new_head)
    return new_head

def check_collision(snake):
    """Checks for wall or self-collision."""
    head_x, head_y = snake[0]
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        return True
    if snake[0] in snake[1:]:
        return True
    return False

def draw_game(snake, food_position, color):
    """Draws the snake, food, and background."""
    if color == 1:
        screen.fill(WHITE)
    else:
        screen.fill(BLACK)
    for segment in snake:
        if segment == snake[0]:
            color = LIGHT_GREEN
        else:
            color = GREEN
        pygame.draw.rect(screen, color, (*segment, BLOCK_SIZE, BLOCK_SIZE))
    
    pygame.draw.rect(screen, RED, (*food_position, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.flip()

def run_game(difficulty, high_score):
    """Runs one round of the game and returns the final score."""
    # Set speed based on difficulty
    if difficulty == "EASY":
        FPS = 7.5
    elif difficulty == "MEDIUM":
        FPS = 15
    else:
        FPS = 30

    # Initialize game state
    snake = [(180, 90), (150, 90), (120, 90)]
    direction = (BLOCK_SIZE, 0)
    food_position = spawn_food(snake)
    score = 0
    color = 0
    paused = False

    pygame.display.set_caption(f"Snake Game  |  Difficulty: {difficulty}  |  Press SPACE to Pause  |  Score: {score}")

    running = True
    while running:
        clock.tick(FPS)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_f:
                    color += 1
                    color %= 2
                if not paused:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != (0, BLOCK_SIZE):
                        direction = (0, -BLOCK_SIZE)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != (0, -BLOCK_SIZE):
                        direction = (0, BLOCK_SIZE)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != (BLOCK_SIZE, 0):
                        direction = (-BLOCK_SIZE, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != (-BLOCK_SIZE, 0):
                        direction = (BLOCK_SIZE, 0)

        # Pause behavior
        if paused:
            font = pygame.font.Font(None, 60)
            pause_text = font.render("PAUSED", True, BLACK)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            continue

        # Move snake
        new_head = move_snake(snake, direction)

        # Check collision
        if check_collision(snake):
            running = False
            continue

        # Eat food or move normally
        if new_head == food_position:
            food_position = spawn_food(snake)
            score += 1
            pygame.display.set_caption(f"Snake Game  |  Difficulty: {difficulty}  |  Press SPACE to Pause  |  Score: {score}")
        else:
            snake.pop()

        # Draw everything
        draw_game(snake, food_position, color)

    return score

# MAIN LOOP
def main():
    """Main Driver Function"""
    difficulty = start_menu()
    high_score = 0
    playing = True
    while playing:
        score = run_game(difficulty, high_score)
        high_score = max(high_score, score)
        playing = game_over_menu(score, high_score)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
