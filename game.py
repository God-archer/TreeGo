import pygame
from board import Board
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_GRAY, PLAYER_GREEN, VICTORY_CONDITION, BOARD_WIDTH, \
    BOARD_HEIGHT, WHITE, BLACK, RED, GRID_SIZE


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_player = PLAYER_GRAY  # 灰方先行
        self.game_over = False
        self.winner = None
        self.victory_conditions_met = False
        self.width = self.board.width  # 添加棋盘宽度
        self.height = self.board.height  # 添加棋盘高度
        self.green_count_in_gray_root = 0
        self.gray_count_in_green_root = 0

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.handle_click(event.pos)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_click(self, pos):
        x, y = pos
        # 转换为棋盘坐标
        grid_x = x // GRID_SIZE
        grid_y = y // GRID_SIZE
        self.place_piece(grid_x, grid_y)

    def place_piece(self, x, y):
        # 检查是否可落子
        if self.board.board[y][x][1] is None and self.is_valid_position(x, y):
            # 放置“叶”棋子
            if self.current_player == PLAYER_GRAY:
                self.board.board[y][x] = (None, 'gray_leaf')
            else:
                self.board.board[y][x] = (None, 'green_leaf')
            # 切换玩家
            self.current_player = PLAYER_GREEN if self.current_player == PLAYER_GRAY else PLAYER_GRAY

    def is_valid_position(self, x, y):
        # 检查是否在棋盘内
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # 检查是否在自己的根源区域
        if self.current_player == PLAYER_GRAY:
            # 灰方玩家不能在自己的根源区域落子
            if y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4):
                return False
        else:
            # 青方玩家不能在自己的根源区域落子
            if y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4):
                return False

        # 检查是否在“叶”棋子周围
        if self.current_player == PLAYER_GRAY:
            leaf_color = 'gray_leaf'
        else:
            leaf_color = 'green_leaf'

        # 检查周围八个格子是否有“叶”棋子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # 检查周围格子是否在根源区域
                    if not self.is_growable(nx, ny):
                        continue  # 如果在根源区域，跳过该格子
                    if self.board.board[ny][nx][1] == leaf_color:
                        return True
        return False

    def is_growable(self, x, y):
        # 检查棋子是否在对方的根源区域
        if self.current_player == PLAYER_GRAY:
            return not (y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4))
        else:
            return not (y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4))

    def is_green_root_area(self, y, x):
        # 检查是否在青方根源区域内
        return y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4)

    def is_gray_root_area(self, y, x):
        # 检查是否在灰方根源区域内
        return y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4)

    def draw(self):
        self.screen.fill(WHITE)
        self.board.draw(self.screen)
        # 显示当前玩家
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Player: {'Gray' if self.current_player == PLAYER_GRAY else 'Green'}", True, BLACK)
        self.screen.blit(text, (10, 10))
        # 显示胜利信息
        if self.game_over:
            text = font.render(f"Player {'Gray' if self.winner == PLAYER_GRAY else 'Green'} wins!", True, RED)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))