import pygame
from board import Board
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_GRAY, PLAYER_GREEN, VICTORY_CONDITION, BOARD_WIDTH, \
    BOARD_HEIGHT, WHITE, BLACK, GRID_SIZE, LIGHT_GRAY, LIGHT_GREEN, DARK_GRAY, DARK_GREEN, GREEN, RED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.board.game = self  # 设置Board实例的game引用
        self.current_player = PLAYER_GRAY  # 灰方先行
        self.game_over = False
        self.winner = None
        self.victory_conditions_met = False
        self.width = self.board.width  # 添加棋盘宽度
        self.height = self.board.height  # 添加棋盘高度
        self.green_count_in_gray_root = 0
        self.gray_count_in_green_root = 0
        self.gray_branch_used = False  # 灰方枝棋子是否已使用
        self.green_branch_used = False  # 青方枝棋子是否已使用
        self.gray_branch_cooldown = False  # 灰方枝棋子是否在冷却中
        self.green_branch_cooldown = False  # 青方枝棋子是否在冷却中
        self.gray_trunk_used = False  # 灰方干棋子是否已使用
        self.green_trunk_used = False  # 青方干棋子是否已使用
        self.gray_trunk_cooldown = False  # 灰方干棋子是否在冷却中
        self.green_trunk_cooldown = False  # 青方干棋子是否在冷却中
        self.selected_piece_type = 'leaf'  # 当前选择的棋子类型：'leaf', 'branch', 'trunk'
        self.gray_pieces = ['gray_leaf', 'gray_branch', 'gray_trunk']
        self.green_pieces = ['green_leaf', 'green_branch', 'green_trunk']
        self.victory_display_timer = 0  # 胜利显示计时器
        self.victory_display_duration = 3000  # 胜利显示持续时间（毫秒）

    def run(self):
        while True:  # 修改为无限循环
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:  # 如果按下鼠标
                    self.handle_click(event.pos)  # 尝试进行落子

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # 检查游戏结束条件
            if self.game_over:
                if self.winner:
                    # 如果是胜利结束，显示胜利画面
                    current_time = pygame.time.get_ticks()
                    if self.victory_display_timer == 0:
                        self.victory_display_timer = current_time
                    elif current_time - self.victory_display_timer >= self.victory_display_duration:
                        return
                else:
                    # 如果是点击返回按钮结束，直接返回
                    return

    def handle_click(self, pos):
        x, y = pos
        # 检查是否点击了返回按钮
        if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(pos):
            self.game_over = True
            return
            
        # 检查是否点击了棋子选择按钮
        button_y = SCREEN_HEIGHT - 60
        if button_y <= y <= button_y + 40:
            button_x = (x - 10) // 120
            if 0 <= button_x <= 2:
                piece_types = ['leaf', 'branch', 'trunk']
                if button_x < len(piece_types):
                    self.selected_piece_type = piece_types[button_x]
                return
        
        # 转换为棋盘坐标并尝试落子
        grid_x = x // GRID_SIZE
        grid_y = y // GRID_SIZE
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self.place_piece(grid_x, grid_y)

    def place_piece(self, x, y):
        # 检查是否可落子
        if self.board.board[y][x][1] is None and self.is_valid_position(x, y):
            piece_prefix = 'gray' if self.current_player == PLAYER_GRAY else 'green'
            piece_type = f'{piece_prefix}_{self.selected_piece_type}'
            
            # 检查特殊棋子的使用限制
            if self.selected_piece_type == 'branch':
                if piece_prefix == 'gray':
                    if self.gray_branch_used or self.gray_branch_cooldown:
                        return  # 已使用过枝棋子或在冷却中
                    self.gray_branch_used = True
                else:
                    if self.green_branch_used or self.green_branch_cooldown:
                        return  # 已使用过枝棋子或在冷却中
                    self.green_branch_used = True
            elif self.selected_piece_type == 'trunk':
                if piece_prefix == 'gray':
                    if self.gray_trunk_used or self.gray_trunk_cooldown:
                        return  # 已使用过干棋子或在冷却中
                    self.gray_trunk_used = True
                else:
                    if self.green_trunk_used or self.green_trunk_cooldown:
                        return  # 已使用过干棋子或在冷却中
                    self.green_trunk_used = True
            
            # 放置棋子
            self.board.board[y][x] = (self.board.board[y][x][0], piece_type)

            # 更新冷却
            self.update_cooldown()

            # 推动逻辑
            self.push_pieces(x, y)

            # 消除逻辑
            self.eliminate_pieces()

            # 判定胜利
            if self.is_win():
                self.game_over = True
                self.winner = self.current_player
                return

            # 切换玩家
            self.switch_player()

            # 判定胜利
            if self.is_win():
                self.game_over = True
                self.winner = self.current_player
                return

    def update_cooldown(self):
        if self.current_player == PLAYER_GRAY:
            self.gray_branch_cooldown = False
            self.gray_trunk_cooldown = False
        else:
            self.green_branch_cooldown = False
            self.green_trunk_cooldown = False

    def switch_player(self):
        # 切换玩家
        self.current_player = PLAYER_GREEN if self.current_player == PLAYER_GRAY else PLAYER_GRAY

    def eliminate_pieces(self):
        # 获取当前玩家和敌方玩家的棋子颜色，根源颜色
        if self.current_player == PLAYER_GRAY:
            player_pieces = ['gray_leaf', 'gray_branch', 'gray_trunk']
            enemy_pieces = ['green_leaf', 'green_branch', 'green_trunk']
            player_root = "gray_root"
            enemy_root = "green_root"
        else:
            player_pieces = ['green_leaf', 'green_branch', 'green_trunk']
            enemy_pieces = ['gray_leaf', 'gray_branch', 'gray_trunk']
            player_root = "green_root"
            enemy_root = "gray_root"

        # 检查纵向消除（当前玩家）
        for x in range(self.width):
            count = 0
            root_count = 0
            for y in range(self.height):
                if self.board.board[y][x][1] in player_pieces:
                    count += 1
                    if self.is_in_root(x, y):
                        root_count += 1

                else:
                    count = 0
                    root_count = 0

                if root_count > 1:
                    count = 0
                    root_count = 0

                if count >= 3:
                    # 消除从 y-2 到 y 的棋子
                    for i in range(y - 2, y + 1):
                        piece_type = self.board.board[i][x][1]
                        self.board.board[i][x] = (self.board.board[i][x][0], None)
                        # 设置冷却状态
                        if piece_type == 'gray_branch':
                            self.gray_branch_used = False
                            self.gray_branch_cooldown = True
                        elif piece_type == 'green_branch':
                            self.green_branch_used = False
                            self.green_branch_cooldown = True
                        elif piece_type == 'gray_trunk':
                            self.gray_trunk_used = False
                            self.gray_trunk_cooldown = True
                        elif piece_type == 'green_trunk':
                            self.green_trunk_used = False
                            self.green_trunk_cooldown = True

        # 检查横向消除（当前玩家）
        for y in range(self.height):
            count = 0
            root_count = 0
            for x in range(self.width):
                if self.board.board[y][x][1] in player_pieces:
                    count += 1
                    if self.is_in_root(x, y):
                        root_count += 1

                else:
                    count = 0
                    root_count = 0

                if root_count > 1:
                    count = 0
                    root_count = 0

                if count >= 3:
                    # 消除从 x-2 到 x 的棋子
                    for i in range(x - 2, x + 1):
                        piece_type = self.board.board[y][i][1]
                        self.board.board[y][i] = (self.board.board[y][i][0], None)
                        # 设置冷却状态
                        if piece_type == 'gray_branch':
                            self.gray_branch_used = False
                            self.gray_branch_cooldown = True
                        elif piece_type == 'green_branch':
                            self.green_branch_used = False
                            self.green_branch_cooldown = True
                        elif piece_type == 'gray_trunk':
                            self.gray_trunk_used = False
                            self.gray_trunk_cooldown = True
                        elif piece_type == 'green_trunk':
                            self.green_trunk_used = False
                            self.green_trunk_cooldown = True

        # 检查纵向消除（敌方玩家）
        for x in range(self.width):
            count = 0
            root_count = 0
            for y in range(self.height):
                if self.board.board[y][x][1] in enemy_pieces:
                    count += 1
                    if self.is_in_root(x, y):
                        root_count += 1

                else:
                    count = 0
                    root_count = 0

                if root_count > 1:
                    count = 0
                    root_count = 0

                if count >= 3:
                    # 消除从 y-2 到 y 的棋子
                    for i in range(y - 2, y + 1):
                        piece_type = self.board.board[i][x][1]
                        self.board.board[i][x] = (self.board.board[i][x][0], None)
                        # 设置冷却状态
                        if piece_type == 'gray_branch':
                            self.gray_branch_used = False
                            self.gray_branch_cooldown = True
                        elif piece_type == 'green_branch':
                            self.green_branch_used = False
                            self.green_branch_cooldown = True
                        elif piece_type == 'gray_trunk':
                            self.gray_trunk_used = False
                            self.gray_trunk_cooldown = True
                        elif piece_type == 'green_trunk':
                            self.green_trunk_used = False
                            self.green_trunk_cooldown = True

        # 检查横向消除（敌方玩家）
        for y in range(self.height):
            count = 0
            root_count = 0
            for x in range(self.width):
                if self.board.board[y][x][1] in enemy_pieces:
                    count += 1
                    if self.is_in_root(x, y):
                        root_count += 1

                else:
                    count = 0
                    root_count = 0

                if root_count > 1:
                    count = 0
                    root_count = 0

                if count >= 3:
                    # 消除从 x-2 到 x 的棋子
                    for i in range(x - 2, x + 1):
                        piece_type = self.board.board[y][i][1]
                        self.board.board[y][i] = (self.board.board[y][i][0], None)
                        # 设置冷却状态
                        if piece_type == 'gray_branch':
                            self.gray_branch_used = False
                            self.gray_branch_cooldown = True
                        elif piece_type == 'green_branch':
                            self.green_branch_used = False
                            self.green_branch_cooldown = True
                        elif piece_type == 'gray_trunk':
                            self.gray_trunk_used = False
                            self.gray_trunk_cooldown = True
                        elif piece_type == 'green_trunk':
                            self.green_trunk_used = False
                            self.green_trunk_cooldown = True

    def push_pieces(self, x, y):
        # 获取当前玩家的敌方玩家
        if self.current_player == PLAYER_GRAY:
            enemy_pieces = ['green_leaf', 'green_branch']
        else:
            enemy_pieces = ['gray_leaf', 'gray_branch']

        # 检查四个方向是否有敌方棋子
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.board.board[ny][nx][1] in enemy_pieces:
                    # 推动敌方棋子
                    self.push_enemy_piece(nx, ny, dx, dy)

    def push_enemy_piece(self, x, y, dx, dy):
        # 获取当前玩家的敌方棋子颜色
        if self.current_player == PLAYER_GRAY:
            enemy_pieces = ['green_leaf', 'green_branch']
        else:
            enemy_pieces = ['gray_leaf', 'gray_branch']

        # 检查敌方棋子是否存在
        if self.board.board[y][x][1] not in enemy_pieces:
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
            if self.board.board[next_y][next_x][1] in enemy_pieces:
                current_x, current_y = next_x, next_y
            else:
                break  # 无法继续推动

        # 如果链式移动列表为空，直接返回
        if not push_chain:
            return

        # 计算最后一位棋子的新位置
        new_y, new_x = current_y + dy, current_x + dx
        # 检查新位置是否在对方根源区域
        if self.is_in_opponent_root(new_x, new_y):
            # 不能把对方的棋子推到对方根源区域
            return

        # 检查新位置是否在棋盘内且为空
        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.board.board[new_y][new_x][1] is None:
            # 更新最后一个棋子的位置，保留根源区域信息
            self.board.board[new_y][new_x] = (self.board.board[new_y][new_x][0], self.board.board[current_y][current_x][1])
            self.board.board[current_y][current_x] = (self.board.board[current_y][current_x][0], None)
            # 更新其他棋子的位置
            for i in range(len(push_chain) - 1, -1, -1):
                if i == 0:
                    prev_x, prev_y = x, y
                else:
                    prev_x, prev_y = push_chain[i - 1]
                current_x, current_y = push_chain[i]
                self.board.board[current_y][current_x] = (self.board.board[current_y][current_x][0], self.board.board[prev_y][prev_x][1])
                self.board.board[prev_y][prev_x] = (self.board.board[prev_y][prev_x][0], None)
        else:
            # 如果无法推动到最后一个位置，整条链式移动失败
            pass

    def is_in_opponent_root(self, x, y):
        if self.current_player == PLAYER_GRAY:
            # 灰方玩家检查是否在青方根源区域
            return y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4)
        else:
            # 青方玩家检查是否在灰方根源区域
            return y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4)

    def is_in_root(self, x, y):
        return (y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4)) or (y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4))

    def is_win(self):
        # 检查一般胜利条件：占领对方根源区域
        if self.current_player == PLAYER_GRAY:
            for x in range(self.width // 4, self.width * 3 // 4):
                if self.board.board[0][x][1] not in self.gray_pieces:
                    break
            else:
                return True
        else:
            for x in range(self.width // 4, self.width * 3 // 4):
                if self.board.board[BOARD_HEIGHT-1][x][1] not in self.green_pieces:
                    break
            else:
                return True

        # 检查特殊胜利条件：根源区域外没有敌方棋子
        enemy_pieces = self.green_pieces if self.current_player == PLAYER_GRAY else self.gray_pieces
        for y in range(self.height):
            for x in range(self.width):
                # 跳过自己的根源区域
                if self.current_player == PLAYER_GRAY and y == self.height - 1 and (x >= self.width // 4 and x < self.width * 3 // 4):
                    continue
                if self.current_player == PLAYER_GREEN and y == 0 and (x >= self.width // 4 and x < self.width * 3 // 4):
                    continue
                # 检查是否存在敌方棋子
                if self.board.board[y][x][1] in enemy_pieces:
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

        # 定义本方颜色
        if self.current_player == PLAYER_GRAY:
            leaf_color = 'gray_leaf'
            branch_color = 'gray_branch'
            trunk_color = 'gray_trunk'
        else:
            leaf_color = 'green_leaf'
            branch_color = 'green_branch'
            trunk_color = 'green_trunk'

        # 检查是否在枝棋子的5x3范围内
        if self.is_branch_valid_position(x, y):
            return True

        # 检查周围八个格子是否有"叶"棋子或“干”棋子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # 检查周围格子是否在根源区域
                    if not self.is_growable(nx, ny):
                        continue  # 如果在根源区域，跳过该格子
                    if self.board.board[ny][nx][1] == leaf_color or self.board.board[ny][nx][1] == trunk_color:
                        return True
        return False

    def is_branch_valid_position(self, x, y):
        # 检查是否可以放置枝棋子
        if self.current_player == PLAYER_GRAY:
            branch_color = 'gray_branch'
        else:
            branch_color = 'green_branch'

        # 遍历棋盘寻找枝棋子
        branch_x = None
        branch_y = None
        for i in range(self.height):
            for j in range(self.width):
                if self.board.board[i][j][1] == branch_color:
                    branch_y = i
                    branch_x = j
                    break
            if branch_x is not None:
                break

        if branch_x is None:
            return False

        # 检查是否在枝棋子的5x3范围内
        dx = abs(x - branch_x)
        dy = abs(y - branch_y)
        return dx <= 2 and dy <= 1  # 5x3范围（中心点左右各2格，上下各1格）

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
        
        # 显示当前玩家和选择的棋子类型
        font = pygame.font.Font("c:\Windows\Fonts\msyh.ttc", 18)  # 使用微软雅黑字体
        player_text = f"当前玩家：{'灰方' if self.current_player == PLAYER_GRAY else '青方'}"
        # # 已被棋子选择系统代替
        # piece_text = f"当前棋子：{'叶' if self.selected_piece_type == 'leaf' else '枝' if self.selected_piece_type == 'branch' else '干'}"
        
        player_surface = font.render(player_text, True, BLACK)
        # piece_surface = font.render(piece_text, True, BLACK)
        
        self.screen.blit(player_surface, (10, 10))
        
        # 绘制返回按钮
        back_button_rect = pygame.Rect(10, 40, 80, 30)
        pygame.draw.rect(self.screen, WHITE, back_button_rect)
        pygame.draw.rect(self.screen, BLACK, back_button_rect, 2)
        back_text = font.render("返回", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
        self.back_button_rect = back_button_rect  # 存储返回按钮位置供点击检测使用
        
        # 绘制棋子选择按钮
        button_y = SCREEN_HEIGHT - 60
        for i, piece_type in enumerate(['leaf', 'branch', 'trunk']):
            button_rect = pygame.Rect(10 + i * 120, button_y, 100, 40)
            color = GREEN if self.selected_piece_type == piece_type else WHITE
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            piece_name = '叶' if piece_type == 'leaf' else '枝' if piece_type == 'branch' else '干'
            text = font.render(piece_name, True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        # 显示胜利信息
        if self.game_over and self.winner:
            # 创建半透明背景
            overlay = pygame.Surface((300, 100), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 128), overlay.get_rect())
            overlay_rect = overlay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(overlay, overlay_rect)
            
            # 绘制边框
            pygame.draw.rect(self.screen, BLACK, overlay_rect, 2)
            
            # 显示胜利文本
            font = pygame.font.Font("c:\Windows\Fonts\msyh.ttc", 36)  # 使用更大的字体
            text = font.render(f"{'灰方' if self.winner == PLAYER_GRAY else '青方'} 胜利!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            # 删除多余的渲染代码
