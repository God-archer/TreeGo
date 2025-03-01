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
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:  # 如果按下鼠标
                    self.handle_click(event.pos)  # 尝试进行落子
                    if self.is_win():  # 判定是否胜利
                        self.game_over = True
                        self.winner = self.current_player
                    self.current_player = PLAYER_GREEN if self.current_player == PLAYER_GRAY else PLAYER_GRAY   # 切换玩家
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

            # 推动逻辑
            self.push_pieces(x, y)

    def push_pieces(self, x, y):
        # 获取当前玩家的敌方玩家
        if self.current_player == PLAYER_GRAY:
            enemy_piece = 'green_leaf'
        else:
            enemy_piece = 'gray_leaf'

        # 检查四个方向是否有敌方棋子
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.board.board[ny][nx][1] == enemy_piece:
                    # 推动敌方棋子
                    self.push_enemy_piece(nx, ny, dx, dy)

    def push_enemy_piece(self, x, y, dx, dy):
        # 获取当前玩家的敌方棋子颜色
        if self.current_player == PLAYER_GRAY:
            enemy_piece = 'green_leaf'
        else:
            enemy_piece = 'gray_leaf'

        # 检查敌方棋子是否存在
        if self.board.board[y][x][1] != enemy_piece:
            return

        # 创建一个列表来存储需要推动的棋子的位置
        push_chain = []
        current_x, current_y = x, y
        while True:
            # 添加当前棋子到链式移动列表中
            push_chain.append((current_x, current_y))
            # 计算下一个位置
            next_x = current_x + dx
            next_y = current_y + dy
            # 检查是否超出棋盘范围
            if next_x < 0 or next_x >= self.width or next_y < 0 or next_y >= self.height:
                break
            # 检查下一个位置是否有敌方棋子
            if self.board.board[next_y][next_x][1] == enemy_piece:
                current_x, current_y = next_x, next_y
            else:
                break  # 无法继续推动

        # 如果链式移动列表为空，直接返回
        if not push_chain:
            return

        # 计算最后一位棋子的新位置
        new_y, new_x = current_y + dy, current_x + dx
        # 检查新位置是否在己方根源区域
        if self.is_in_own_root(new_x, new_y):
            # 不能推到己方根源区域
            return

        # 检查新位置是否在棋盘内且为空
        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.board.board[new_y][new_x][1] is None:
            # 更新最后一个棋子的位置
            self.board.board[new_y][new_x] = self.board.board[current_y][current_x]
            self.board.board[current_y][current_x] = (None, None)
            # 更新其他棋子的位置
            for i in range(len(push_chain) - 1, -1, -1):
                if i == 0:
                    prev_x, prev_y = x, y
                else:
                    prev_x, prev_y = push_chain[i - 1]
                current_x, current_y = push_chain[i]
                self.board.board[current_y][current_x] = self.board.board[prev_y][prev_x]
                self.board.board[prev_y][prev_x] = (None, None)
        else:
            # 如果无法推动到最后一个位置，整条链式移动失败
            pass

    def is_in_own_root(self, x, y):
        if self.current_player == PLAYER_GRAY:
            # 灰方玩家检查是否在青方根源区域
            return y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4)
        else:
            # 青方玩家检查是否在灰方根源区域
            return y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4)

    def is_win(self):
        if self.current_player == PLAYER_GRAY:
            for x in range(self.width // 4, self.width * 3 // 4):
                if self.board.board[0][x][1] != 'gray_leaf':
                    return False
        else:
            for x in range(self.width // 4, self.width * 3 // 4):
                if self.board.board[BOARD_HEIGHT-1][x][1] != 'green_leaf':
                    return False
        return True

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
            print(f"Player {'Gray' if self.winner == PLAYER_GRAY else 'Green'} wins!")
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
