import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# 设置游戏窗口大小
WINDOW_X = 800
WINDOW_Y = 600

# 初始化游戏窗口
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('贪吃蛇游戏')

# 定义蛇的属性
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# 初始化时钟
clock = pygame.time.Clock()

def draw_snake(snake_list):
    """绘制蛇的身体"""
    for block in snake_list:
        pygame.draw.rect(game_window, GREEN, [block[0], block[1], SNAKE_BLOCK, SNAKE_BLOCK])

def generate_food():
    """生成随机食物位置"""
    food_x = round(random.randrange(0, WINDOW_X - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, WINDOW_Y - SNAKE_BLOCK) / 10.0) * 10.0
    return food_x, food_y

def main():
    """主游戏循环"""
    running = True
    game_over = False

    # 初始化蛇的位置和长度
    snake_list = []
    length_of_snake = 1
    snake_x = WINDOW_X // 2
    snake_y = WINDOW_Y // 2
    snake_dx = 0
    snake_dy = 0

    # 初始化食物位置
    food_x, food_y = generate_food()

    while running:
        while game_over:
            game_window.fill(BLACK)
            font = pygame.font.SysFont(None, 50)
            message = font.render("Game Over! Press R to Restart", True, RED)
            game_window.blit(message, [WINDOW_X // 6, WINDOW_Y // 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()

        for event in pygame.event.get():            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_dx == 0:
                    snake_dx = -SNAKE_BLOCK
                    snake_dy = 0
                elif event.key == pygame.K_RIGHT and snake_dx == 0:
                    snake_dx = SNAKE_BLOCK
                    snake_dy = 0
                elif event.key == pygame.K_UP and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = SNAKE_BLOCK

        # 更新蛇的位置
        snake_x += snake_dx
        snake_y += snake_dy

        # 检查边界碰撞
        if snake_x < 0 or snake_x >= WINDOW_X or snake_y < 0 or snake_y >= WINDOW_Y:
            game_over = True

        # 检查是否吃到食物
        if snake_x == food_x and snake_y == food_y:
            food_x, food_y = generate_food()
            length_of_snake += 1

        # 更新蛇的身体
        snake_list.append([snake_x, snake_y])
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # 检查是否碰到自己
        for block in snake_list[:-1]:
            if block == [snake_x, snake_y]:
                game_over = True

        # 绘制游戏元素
        game_window.fill(BLACK)
        pygame.draw.rect(game_window, GREEN, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        draw_snake(snake_list)
        pygame.display.update()

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()