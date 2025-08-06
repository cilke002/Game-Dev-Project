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
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
LIGHT_GREEN = (0, 255, 0)

# Screen display 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up clock
clock = pygame.time.Clock()

# Start menu
def start_menu():
    font = pygame.font.Font(None, 50)
    title_text = font.render("SNAKE GAME", True, GREEN)
    select_text = font.render("Select Difficulty", True, WHITE)
    easy_text = font.render("EASY", True, GREEN)
    medium_text = font.render("MEDIUM", True, BLUE)
    hard_text = font.render("HARD", True, RED)
    easy_mode = easy_text.get_rect(center=(WIDTH // 2, 400 + easy_text.get_height() // 2))
    medium_mode = medium_text.get_rect(center=(WIDTH // 2, 450 + medium_text.get_height() // 2))
    hard_mode = hard_text.get_rect(center=(WIDTH // 2, 500 + hard_text.get_height() // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 8))
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - easy_text.get_height() - 20))
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 400))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 450))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 500))
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
                
# Game over menu                
def game_over_menu():
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render("SCORE: " + str(score), True, WHITE)
    high_score_text = font.render("HIGH SCORE: " + str(high_score), True, LIGHT_BLUE)
    continue_text = font.render("Continue?", True, WHITE)
    yes_text = font.render("YES", True, GREEN)
    no_text = font.render("NO", True, RED)
    yes_box = yes_text.get_rect(center = (WIDTH // 2 - 50, 550 + yes_text.get_height() // 2))
    no_box = no_text.get_rect(center = (WIDTH // 2 + 50, 550 + no_text.get_height() // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 25))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 75))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - 50 - high_score_text.get_height() // 2))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(yes_text, (WIDTH // 2 - yes_text.get_width() // 2 - 50, 550))
        screen.blit(no_text, (WIDTH // 2 - no_text.get_width() // 2 + 50, 550))
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
                
# Spawn food
def spawn_food(snake):
    max_x = WIDTH // BLOCK_SIZE
    max_y = HEIGHT // BLOCK_SIZE

    while True:
        food_x = random.randint(0, max_x - 1) * BLOCK_SIZE
        food_y = random.randint(0, max_y - 1) * BLOCK_SIZE
        if (food_x, food_y) not in snake:
            return (food_x, food_y)


# Start up game and select difficulty
difficulty = start_menu()
if difficulty == "EASY":
    FPS = 10
elif difficulty == "MEDIUM":
    FPS = 15
else:
    FPS = 30

# Play Snake for as long as player likes on selected difficulty
playing = True
high_score = 0
while playing:

    # Reset game state at the start of each new game
    snake = [(180, 90), (150, 90), (120, 90), (90, 90), (60, 90), (30, 90)]
    direction = (BLOCK_SIZE, 0)
    food_position = spawn_food(snake)
    score = 0
    pygame.display.set_caption("Snake Game          Difficulty: " + difficulty + "          Press SPACE to PAUSE          Score: " + str(score))
    paused = False
    running = True

    # Run each game
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if not paused:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != (0, BLOCK_SIZE):
                        direction = (0, -BLOCK_SIZE)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != (0, -BLOCK_SIZE):
                        direction = (0, BLOCK_SIZE)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != (BLOCK_SIZE, 0):
                        direction = (-BLOCK_SIZE, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != (-BLOCK_SIZE, 0):
                        direction = (BLOCK_SIZE, 0)

        # Skip movement and game logic if paused
        if paused:

            # Draw pause text
            font = pygame.font.Font(None, 60)
            pause_text = font.render("PAUSED", True, BLACK)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            continue  # Skip rest of loop until unpaused

        # Calculate new snake head after movement
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Check for collisions
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake
        ):
            running = False
            continue  # Skip rest of loop so we don't modify snake

        # Move snake
        snake.insert(0, new_head)

        # Eat food or move normally
        if new_head == food_position:
            food_position = spawn_food(snake)
            score += 1
            pygame.display.set_caption("Snake Game          Difficulty: " + difficulty + "          Press SPACE to PAUSE          Score: " + str(score))
        else:
            snake.pop()

        # Background
        screen.fill(WHITE)

        # Draw snake
        for segment in snake:
            if segment == snake[0]:
                pygame.draw.rect(screen, LIGHT_GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, (*food_position, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()

    # Game over screen, continue? (y/n)
    if score > high_score:
        high_score = score
    playing = game_over_menu()

# Quit
pygame.quit()
sys.exit()
