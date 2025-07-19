import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Game window setup
screen_width = 1540
screen_height = 800
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FEED THE BOX")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Algerian', 50)

# Ensure high score file exists and has at least 0
if not os.path.exists('High_score.txt'):
    with open('High_score.txt', 'w') as f:
        f.write("0")

def read_high_score():
    try:
        with open('High_score.txt', 'r') as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else 0
    except:
        return 0

def write_high_score(score):
    with open('High_score.txt', 'w') as f:
        f.write(str(score))

# Display text
def text_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x, y])

# Draw snake
def plot_snake(gameWindow, colour, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, colour, [x, y, snake_size, snake_size])

def game_loop():
    high_score = read_high_score()
    exit_game = False
    game_over = False

    # Snake setup
    box_x = 40
    box_y = 60
    velocity_x = 5
    velocity_y = 0
    snake_size = 30
    snk_list = []
    snk_length = 1

    # Food setup
    circle_radius = 10
    circle_x = random.randint(200, screen_width - circle_radius)
    circle_y = random.randint(200, screen_height - circle_radius)

    score = 0
    fps = 30

    while not exit_game:
        if game_over:
            gameWindow.fill(white)

            if score >= high_score:
                high_score = score
                write_high_score(high_score)

            # Show game over and high score
            text1 = "Game Over! Press ENTER to Restart"
            text2 = f"High Score: {high_score}"

            t1_w, t1_h = font.size(text1)
            t2_w, t2_h = font.size(text2)
            

            text_screen(text1, red, (screen_width - t1_w)//2, screen_height//2 - 50)
            text_screen(text2, black, (screen_width - t2_w)//2, screen_height//2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_loop()
                    return

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -5
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = 5
                        velocity_x = 0

            box_x += velocity_x
            box_y += velocity_y

            gameWindow.fill(white)
            pygame.draw.circle(gameWindow, red, (circle_x, circle_y), circle_radius)

            head = [box_x, box_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if (head in snk_list[:-1] or box_x < 0 or box_x > screen_width or box_y < 0 or box_y > screen_height):
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
            text_screen(f"Score: {score}", black, 50, 20)

            if abs(box_x - circle_x) < 20 and abs(box_y - circle_y) < 20:
                score += 1
                snk_length += 5
                circle_x = random.randint(200, screen_width - circle_radius)
                circle_y = random.randint(200, screen_height - circle_radius)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

game_loop()
