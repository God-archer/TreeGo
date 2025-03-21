# TreeGo - A board game
# This file is part of TreeGo
# Copyright (C) 2024 God_archer (1040257528@qq.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
RED = (255, 0, 0)

# 根源区域颜色
LIGHT_GREEN = (144, 238, 144)  # 浅绿色
LIGHT_GRAY = (211, 211, 211)   # 浅灰色

# 棋子颜色
DARK_GREEN = (0, 100, 0)      # 深绿色
DARK_GRAY = (64, 64, 64)      # 深灰色

# 菜单按钮颜色
BUTTON_BG = (70, 130, 180)      # 钢青色
BUTTON_HOVER = (100, 149, 237)  # 矢车菊蓝
BUTTON_SHADOW = (47, 79, 79)    # 深青灰色
BUTTON_TEXT = (255, 255, 255)   # 白色

# 玩家编码
PLAYER_GRAY = 1
PLAYER_GREEN = 2

# 胜利条件
VICTORY_CONDITION = 4  # 4枚进入根源区域