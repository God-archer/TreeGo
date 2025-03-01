import pygame

# 棋盘单元格结构：(cell_type, piece_type)
# cell_type: green_root, gray_root, None
# piece_type: gray_piece, green_piece, None

# 游戏窗体
TITLE = "树棋TreeGo"  # 标题
ICON = pygame.image.load("assets/ICON.jpg")  # 图标

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

# 棋盘大小
GRID_SIZE = 100
BOARD_WIDTH = 8
BOARD_HEIGHT = 8

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 玩家编码
PLAYER_GRAY = 1
PLAYER_GREEN = 2

# 胜利条件
VICTORY_CONDITION = 4  # 4枚进入根源区域