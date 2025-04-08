import pygame
import random
from typing import Set, List, Tuple

# 初始化 Pygame
pygame.init()

# 定义颜色和游戏常量
class GameConstants:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    WINDOW_X = 800
    WINDOW_Y = 600
    SNAKE_BLOCK = 10
    SNAKE_SPEED = 15
    GRID_WIDTH = WINDOW_X // SNAKE_BLOCK
    GRID_HEIGHT = WINDOW_Y // SNAKE_BLOCK

class SnakeGame:
    def __init__(self):
        # 初始化游戏窗口和资源
        self.game_window = pygame.display.set_mode((GameConstants.WINDOW_X, GameConstants.WINDOW_Y))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.game_over_message = self.font.render("Game Over! Press R to Restart", True, GameConstants.RED)
        
        # 初始化游戏状态
        self.reset_game()
        
        # 预计算所有可能的食物位置
        self.all_positions = {(x * GameConstants.SNAKE_BLOCK, y * GameConstants.SNAKE_BLOCK) 
                            for x in range(GameConstants.GRID_WIDTH) 
                            for y in range(GameConstants.GRID_HEIGHT)}
    
    def reset_game(self) -> None:
        """重置游戏状态"""
        self.running = True
        self.game_over = False
        self.snake_positions: Set[Tuple[float, float]] = set()
        self.snake_list: List[Tuple[float, float]] = []
        self.length_of_snake = 1
        self.snake_x = GameConstants.WINDOW_X // 2
        self.snake_y = GameConstants.WINDOW_Y // 2
        self.snake_dx = 0
        self.snake_dy = 0
        self.food_pos = self.generate_food()

    def generate_food(self) -> Tuple[float, float]:
        """使用集合操作高效生成食物位置"""
        available_positions = self.all_positions - self.snake_positions
        if not available_positions:
            return (0, 0)  # 游戏胜利条件
        return random.choice(tuple(available_positions))

    def draw_snake(self) -> None:
        """使用列表推导式高效绘制蛇身"""
        [pygame.draw.rect(self.game_window, GameConstants.GREEN, 
                        [pos[0], pos[1], GameConstants.SNAKE_BLOCK, GameConstants.SNAKE_BLOCK])
         for pos in self.snake_list]

    def handle_input(self) -> None:
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                elif not self.game_over:
                    self._handle_movement_input(event.key)

    def _handle_movement_input(self, key: int) -> None:
        """处理移动输入"""
        if key == pygame.K_LEFT and self.snake_dx == 0:
            self.snake_dx = -GameConstants.SNAKE_BLOCK
            self.snake_dy = 0
        elif key == pygame.K_RIGHT and self.snake_dx == 0:
            self.snake_dx = GameConstants.SNAKE_BLOCK
            self.snake_dy = 0
        elif key == pygame.K_UP and self.snake_dy == 0:
            self.snake_dx = 0
            self.snake_dy = -GameConstants.SNAKE_BLOCK
        elif key == pygame.K_DOWN and self.snake_dy == 0:
            self.snake_dx = 0
            self.snake_dy = GameConstants.SNAKE_BLOCK

    def update_game_state(self) -> None:
        """更新游戏状态"""
        if self.game_over:
            return

        # 更新蛇的位置
        self.snake_x += self.snake_dx
        self.snake_y += self.snake_dy
        current_pos = (self.snake_x, self.snake_y)

        # 检查边界碰撞
        if (self.snake_x < 0 or self.snake_x >= GameConstants.WINDOW_X or
            self.snake_y < 0 or self.snake_y >= GameConstants.WINDOW_Y):
            self.game_over = True
            return

        # 更新蛇身位置集合和列表
        self.snake_list.append(current_pos)
        self.snake_positions.add(current_pos)
        
        # 检查是否吃到食物
        if current_pos == self.food_pos:
            self.length_of_snake += 1
            self.food_pos = self.generate_food()
        else:
            # 如果没吃到食物，移除蛇尾
            if len(self.snake_list) > self.length_of_snake:
                tail_pos = self.snake_list.pop(0)
                self.snake_positions.remove(tail_pos)

        # 检查是否碰到自己（使用集合提高效率）
        if current_pos in set(self.snake_list[:-1]):
            self.game_over = True

    def draw(self) -> None:
        """绘制游戏画面"""
        self.game_window.fill(GameConstants.BLACK)
        
        if self.game_over:
            self.game_window.blit(self.game_over_message, 
                                [GameConstants.WINDOW_X // 6, GameConstants.WINDOW_Y // 3])
        else:
            pygame.draw.rect(self.game_window, GameConstants.GREEN,
                           [self.food_pos[0], self.food_pos[1], 
                            GameConstants.SNAKE_BLOCK, GameConstants.SNAKE_BLOCK])
            self.draw_snake()
        
        pygame.display.update()

    def run(self) -> None:
        """运行游戏主循环"""
        while self.running:
            self.handle_input()
            self.update_game_state()
            self.draw()
            self.clock.tick(GameConstants.SNAKE_SPEED)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()