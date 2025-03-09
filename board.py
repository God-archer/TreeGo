import pygame
from config import GRID_SIZE, BOARD_WIDTH, BOARD_HEIGHT, WHITE, BLACK, GREEN, GRAY, RED, BLUE

class Board:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.board = [[(None, None) for _ in range(self.width)] for _ in range(self.height)]  # 初始化为 (None, None)
        # 初始化棋盘状态
        self.setup_board()

    def setup_board(self):
        # 初始化根源区域
        for y in range(self.height):
            for x in range(self.width):
                if y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4):
                    self.board[y][x] = ('green_root', None)  # 青方根源
                elif y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4):
                    self.board[y][x] = ('gray_root', None)  # 灰方根源
                else:
                    self.board[y][x] = (None, None)  # 普通格子，无棋子

        # 青方初始“叶”棋子
        self.board[1][self.width // 2 - 1] = (None, 'green_leaf')
        self.board[1][self.width // 2] = (None, 'green_leaf')
        # 灰方初始“叶”棋子
        self.board[self.height - 2][self.width // 2 - 1] = (None, 'gray_leaf')
        self.board[self.height - 2][self.width // 2] = (None, 'gray_leaf')

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cell_type, piece = self.board[y][x]
                # 绘制格子
                color = WHITE
                if cell_type == 'green_root':
                    color = GREEN
                elif cell_type == 'gray_root':
                    color = GRAY
                pygame.draw.rect(
                    screen,
                    color,
                    (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                )
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size),
                    1
                )
                # 绘制棋子
                if piece == 'gray_leaf':
                    pygame.draw.circle(
                        screen,
                        RED,  # 灰方棋子颜色（示例用红色）
                        (x * self.grid_size + self.grid_size // 2, y * self.grid_size + self.grid_size // 2),
                        self.grid_size // 2 - 5  # 留出边框
                    )
                elif piece == 'green_leaf':
                    pygame.draw.circle(
                        screen,
                        BLUE,  # 青方棋子颜色（示例用蓝色）
                        (x * self.grid_size + self.grid_size // 2, y * self.grid_size + self.grid_size // 2),
                        self.grid_size // 2 - 5
                    )
                elif piece == 'gray_branch':
                    # 绘制灰方枝棋子（三角形）
                    center_x = x * self.grid_size + self.grid_size // 2
                    center_y = y * self.grid_size + self.grid_size // 2
                    size = self.grid_size // 2 - 5
                    points = [
                        (center_x, center_y - size),  # 顶点
                        (center_x - size, center_y + size),  # 左下
                        (center_x + size, center_y + size)  # 右下
                    ]
                    pygame.draw.polygon(screen, RED, points)
                elif piece == 'green_branch':
                    # 绘制青方枝棋子（三角形）
                    center_x = x * self.grid_size + self.grid_size // 2
                    center_y = y * self.grid_size + self.grid_size // 2
                    size = self.grid_size // 2 - 5
                    points = [
                        (center_x, center_y - size),  # 顶点
                        (center_x - size, center_y + size),  # 左下
                        (center_x + size, center_y + size)  # 右下
                    ]
                    pygame.draw.polygon(screen, BLUE, points)