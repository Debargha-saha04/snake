import pygame
import random
import os
import asyncio

pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Variables
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, black, [x, y, snake_size, snake_size])


async def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 210, 229))
        text_screen("snake pe apka swagat hain", black, 260, 250)
        text_screen("space bar dabaiyye please", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play(-1)  # Loop background music
                    await gameloop()
                    exit_game = True

        pygame.display.update()
        await asyncio.sleep(0)  # Yield to the event loop


async def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 30
    velocity_x = 0
    velocity_y = 0
    vel = 2
    food_x = random.randint(0, screen_width - 100)
    food_y = random.randint(0, screen_height - 100)
    score = 0
    fps = 100
    snk_list = []
    snk_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            text_screen("tu mar gya bhai, yeh bhi na kar paya,", red, 100, 250)
            text_screen("chal phirse try kar", red, 100, 310)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('back.mp3')
                        pygame.mixer.music.play(-1)
                        await gameloop()
                        exit_game = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = vel
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -vel
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -vel
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = vel
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(0, screen_width - 200)
                food_y = random.randint(0, screen_height - 200)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, blue, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)  # Yield to the event loop

    pygame.quit()


async def main():
    await welcome()


# Run the game
asyncio.run(main())
