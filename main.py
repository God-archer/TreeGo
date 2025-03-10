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
from game import Game
from menu import Menu
from config import TITLE, ICON

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(ICON)
    screen = pygame.display.set_mode((800, 800))
    menu = Menu(screen)
    game = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game:
                selected_option = menu.handle_click(event.pos)
                if selected_option == "quit":
                    running = False
                elif selected_option == "local_multiplayer":
                    game = Game()
                    game.run()
                    game = None  # 游戏结束后重置game变量
                    menu = Menu(screen)  # 重新创建菜单实例
        
        if not game:
            menu.draw()
            pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
