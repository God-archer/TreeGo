import pygame
from game import Game
from config import TITLE, ICON

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(ICON)
    game = Game()
    game.run()
    pygame.quit()
