import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1020, 750
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)

# Screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# MENUS
def start_menu():
    """Displays the start menu and returns selected difficulty."""
    font = pygame.font.Font(None, 50)
    title_text = font.render("SNAKE GAME", True, GREEN)
    select_text = font.render("Select Difficulty", True, WHITE)
    easy_text = font.render("EASY", True, GREEN)
    medium_text = font.render("MEDIUM", True, BLUE)
    hard_text = font.render("HARD", True, RED)

    easy_mode = easy_text.get_rect(center=(WIDTH // 2, 400))
    medium_mode = medium_text.get_rect(center=(WIDTH // 2, 450))
    hard_mode = hard_text.get_rect(center=(WIDTH // 2, 500))

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 8))
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(easy_text, easy_mode.topleft)
        screen.blit(medium_text, medium_mode.topleft)
        screen.blit(hard_text, hard_mode.topleft)
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

def game_over_menu(score, high_score):
    """Displays the game over screen and returns True to play again, False to quit."""
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    high_score_text = font.render(f"HIGH SCORE: {high_score}", True, LIGHT_BLUE)
    continue_text = font.render("Continue?", True, WHITE)
    yes_text = font.render("YES", True, GREEN)
    no_text = font.render("NO", True, RED)

    yes_box = yes_text.get_rect(center=(WIDTH // 2 - 50, 550))
    no_box = no_text.get_rect(center=(WIDTH // 2 + 50, 550))

    while True:
        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 25))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 75))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - 50))
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
