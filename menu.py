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
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BUTTON_BG, BUTTON_HOVER, BUTTON_SHADOW, BUTTON_TEXT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("c:\Windows\Fonts\msyh.ttc", 36)  # 使用微软雅黑字体
        self.selected_option = None
        
        # 定义菜单选项
        self.main_options = [
            "本地游戏",
            "联机对战",
            "退出游戏"
        ]
        self.local_options = [
            "双人对战",
            "人机对战",
            "返回"
        ]
        self.current_menu = "main"  # 当前显示的菜单：'main' 或 'local'
        
        # 计算菜单项的位置
        self.main_menu_positions = []
        self.local_menu_positions = []
        self.calculate_positions()
        
        # 提示文本相关
        self.show_coming_soon = False
        self.coming_soon_timer = 0
        self.coming_soon_duration = 1500  # 显示时间（毫秒）
    
    def calculate_positions(self):
        # 主菜单选项位置
        start_y = SCREEN_HEIGHT // 3
        button_width = 200
        button_height = 60
        
        for i in range(len(self.main_options)):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.centerx = SCREEN_WIDTH // 2
            rect.centery = start_y + i * 100
            self.main_menu_positions.append(rect)
        
        # 本地游戏子菜单位置
        for i in range(len(self.local_options)):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.centerx = SCREEN_WIDTH // 2
            rect.centery = start_y + i * 100
            self.local_menu_positions.append(rect)
    
    def draw(self):
        self.screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_menu == "main":
            # 绘制主菜单
            for i, rect in enumerate(self.main_menu_positions):
                # 检查鼠标悬停
                button_color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_BG
                
                # 绘制按钮阴影
                shadow_rect = rect.copy()
                shadow_rect.y += 4
                pygame.draw.rect(self.screen, BUTTON_SHADOW, shadow_rect, border_radius=10)
                
                # 绘制按钮主体
                pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
                
                # 绘制按钮文字
                text = self.font.render(self.main_options[i], True, BUTTON_TEXT)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
        else:
            # 绘制本地游戏子菜单
            for i, rect in enumerate(self.local_menu_positions):
                # 检查鼠标悬停
                button_color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_BG
                
                # 绘制按钮阴影
                shadow_rect = rect.copy()
                shadow_rect.y += 4
                pygame.draw.rect(self.screen, BUTTON_SHADOW, shadow_rect, border_radius=10)
                
                # 绘制按钮主体
                pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
                
                # 绘制按钮文字
                text = self.font.render(self.local_options[i], True, BUTTON_TEXT)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
    
        # 显示"敬请期待"提示
        if self.show_coming_soon:
            current_time = pygame.time.get_ticks()
            if current_time - self.coming_soon_timer < self.coming_soon_duration:
                # 创建半透明的背景
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(overlay, (0, 0, 0, 128), overlay.get_rect())
                self.screen.blit(overlay, (0, 0))

                # 渲染"敬请期待"文本
                coming_soon_text = self.font.render("敬请期待", True, WHITE)
                text_rect = coming_soon_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(coming_soon_text, text_rect)

                # 绘制关闭按钮
                close_button_size = 30
                close_button_rect = pygame.Rect(
                    text_rect.right + 50,  # 位于文本右侧
                    text_rect.centery - close_button_size // 2,  # 垂直居中
                    close_button_size,
                    close_button_size
                )
                # 绘制关闭按钮背景
                pygame.draw.rect(self.screen, BUTTON_BG, close_button_rect, border_radius=5)
                # 绘制叉号
                close_text = self.font.render("×", True, BUTTON_TEXT)
                close_text_rect = close_text.get_rect(center=close_button_rect.center)
                self.screen.blit(close_text, close_text_rect)
                # 存储关闭按钮位置供点击检测使用
                self.close_button_rect = close_button_rect
            else:
                self.show_coming_soon = False
    
    def handle_click(self, pos):
        # 检查是否点击了关闭按钮
        if self.show_coming_soon and hasattr(self, 'close_button_rect') and self.close_button_rect.collidepoint(pos):
            self.show_coming_soon = False
            return None

        if self.current_menu == "main":
            # 检查主菜单点击
            for i, rect in enumerate(self.main_menu_positions):
                if rect.collidepoint(pos):
                    if i == 0:  # 点击"本地游戏"
                        self.current_menu = "local"
                    elif i == 1:  # 点击"联机对战"
                        self.show_coming_soon = True
                        self.coming_soon_timer = pygame.time.get_ticks()
                    elif i == 2:  # 点击"退出游戏"
                        return "quit"
                    return None
        else:
            # 检查本地游戏子菜单点击
            for i, rect in enumerate(self.local_menu_positions):
                if rect.collidepoint(pos):
                    if i == 0:  # 点击"双人对战"
                        return "local_multiplayer"
                    elif i == 1:  # 点击"人机对战"
                        self.show_coming_soon = True
                        self.coming_soon_timer = pygame.time.get_ticks()
                        return None
                    elif i == 2:  # 点击"返回"
                        self.current_menu = "main"
                        return None
        return None