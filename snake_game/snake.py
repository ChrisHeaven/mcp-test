import pygame
import time
import random

pygame.init()

# 定义颜色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 设置游戏窗口大小
window_x = 800
window_y = 600

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('贪吃蛇游戏')

# 定义蛇的属性
snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()

# 定义蛇的初始位置
snake_list = []
length_of_snake = 1

# 定义食物的位置
foodx = round(random.randrange(0, window_x - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, window_y - snake_block) / 10.0) * 10.0

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_window.fill(black)

    pygame.draw.rect(game_window, green, [foodx, foody, snake_block, snake_block])

    pygame.display.update()

    clock.tick(snake_speed)

pygame.quit()
quit()
