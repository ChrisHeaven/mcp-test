import pygame
import random
from typing import Set, List, Tuple, Dict, Optional
from pygame.sprite import Sprite, Group

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

class SnakeSegment(Sprite):
    """蛇身段精灵类"""
    def __init__(self, x: float, y: float, size: int, color: Tuple[int, int, int]):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Food(Sprite):
    """食物精灵类"""
    def __init__(self, x: float, y: float, size: int, color: Tuple[int, int, int]):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class SnakeGame:
    def __init__(self):
        pygame.init()
        # 初始化游戏窗口和资源
        self.game_window = pygame.display.set_mode((GameConstants.WINDOW_X, GameConstants.WINDOW_Y))
        pygame.display.set_caption('贪吃蛇游戏')
        
        # 创建缓冲surface以提高绘制效率
        self.buffer_surface = pygame.Surface(self.game_window.get_size())
        self.buffer_surface = self.buffer_surface.convert()
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.game_over_message = self.font.render("Game Over! Press R to Restart", True, GameConstants.RED)
        
        # 创建精灵组
        self.snake_sprites = Group()
        self.food_sprite = None
        
        # 初始化位置缓存
        self._init_position_cache()
        self.reset_game()

    def _init_position_cache(self) -> None:
        """预计算并缓存所有可能的位置"""
        self.all_positions = [(x * GameConstants.SNAKE_BLOCK, y * GameConstants.SNAKE_BLOCK)
                            for x in range(GameConstants.GRID_WIDTH)
                            for y in range(GameConstants.GRID_HEIGHT)]
        # 创建位置查找字典以加速碰撞检测
        self.position_lookup: Dict[Tuple[float, float], bool] = {}
    
    def reset_game(self) -> None:
        """重置游戏状态"""
        self.running = True
        self.game_over = False
        self.position_lookup.clear()
        self.snake_sprites.empty()
        self.snake_list = []
        self.length_of_snake = 1
        
        # 初始化蛇的位置
        self.snake_x = GameConstants.WINDOW_X // 2
        self.snake_y = GameConstants.WINDOW_Y // 2
        self.snake_dx = 0
        self.snake_dy = 0
        
        # 创建初始蛇身
        initial_segment = SnakeSegment(self.snake_x, self.snake_y, 
                                     GameConstants.SNAKE_BLOCK, GameConstants.GREEN)
        self.snake_sprites.add(initial_segment)
        self.snake_list.append((self.snake_x, self.snake_y))
        self.position_lookup[(self.snake_x, self.snake_y)] = True
        
        # 生成食物
        self._create_food()

    def _create_food(self) -> None:
        """创建新的食物精灵"""
        if self.food_sprite:
            self.food_sprite.kill()
        
        food_pos = self.generate_food()
        self.food_sprite = Food(food_pos[0], food_pos[1],
                              GameConstants.SNAKE_BLOCK, GameConstants.GREEN)

    def generate_food(self) -> Tuple[float, float]:
        """优化的食物生成算法"""
        available_positions = [pos for pos in self.all_positions if pos not in self.position_lookup]
        if not available_positions:
            return (0, 0)
        return random.choice(available_positions)

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
        """优化的游戏状态更新"""
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

        # 检查自身碰撞
        if current_pos in self.position_lookup:
            self.game_over = True
            return

        # 创建新的蛇头
        new_segment = SnakeSegment(self.snake_x, self.snake_y,
                                 GameConstants.SNAKE_BLOCK, GameConstants.GREEN)
        self.snake_sprites.add(new_segment)
        self.snake_list.append(current_pos)
        self.position_lookup[current_pos] = True

        # 检查是否吃到食物
        if (self.snake_x == self.food_sprite.rect.x and 
            self.snake_y == self.food_sprite.rect.y):
            self.length_of_snake += 1
            self._create_food()
        else:
            # 如果没吃到食物，移除蛇尾
            if len(self.snake_list) > self.length_of_snake:
                tail_pos = self.snake_list.pop(0)
                del self.position_lookup[tail_pos]
                # 移除最后一个精灵
                oldest_sprite = next(iter(self.snake_sprites))
                oldest_sprite.kill()

    def draw(self) -> None:
        """优化的绘制函数"""
        # 清空缓冲区
        self.buffer_surface.fill(GameConstants.BLACK)
        
        if self.game_over:
            self.buffer_surface.blit(self.game_over_message,
                                   [GameConstants.WINDOW_X // 6, GameConstants.WINDOW_Y // 3])
        else:
            # 使用精灵组进行绘制
            self.snake_sprites.draw(self.buffer_surface)
            if self.food_sprite:
                self.food_sprite.draw(self.buffer_surface)

        # 将缓冲区内容复制到屏幕
        self.game_window.blit(self.buffer_surface, (0, 0))
        pygame.display.flip()

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