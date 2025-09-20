import tkinter as tk
import tkinter.messagebox
import math
import random
import time
import heapq
from collections import deque

class HexUI:
    COLORS = {
        'background': '#2E3440',
        'primary': '#5E81AC',
        'secondary': '#81A1C1',
        'text': '#ECEFF4',
        'accent': '#D08770',
        'board': '#4C566A',
        'hexagon': '#434C5E',
        'black_piece': '#3B4252',
        'white_piece': '#E5E9F0'
    }
    FONTS = {
        'title': ('Helvetica', 48, 'bold'),
        'button_large': ('Helvetica', 24),
        'button_medium': ('Helvetica', 18),
        'button_small': ('Helvetica', 14),
        'status': ('Helvetica', 14),
        'rules': ('Helvetica', 14)
    }
    @staticmethod
    def create_button(parent, text, command, font=None, bg=None, fg=None, width=15):
        return tk.Button(parent, text=text, command=command,
                         font=font or HexUI.FONTS['button_medium'],
                         bg=bg or HexUI.COLORS['primary'], fg=fg or HexUI.COLORS['text'],
                         activebackground=HexUI.COLORS['accent'], activeforeground=HexUI.COLORS['text'],
                         borderwidth=0, highlightthickness=0, width=width, relief='flat')
    @staticmethod
    def create_menu_frame(root):
        return tk.Frame(root, bg=HexUI.COLORS['background'])
    @staticmethod
    def create_title_label(parent, text):
        return tk.Label(parent, text=text, font=HexUI.FONTS['title'],
                        bg=HexUI.COLORS['background'], fg=HexUI.COLORS['text'])
    @staticmethod
    def create_rules_window(parent):
        if getattr(parent, "_rules_win", None) and parent._rules_win.winfo_exists():
            parent._rules_win.lift()
            parent._rules_win.focus_force()
            return parent._rules_win

        rules_win = tk.Toplevel(parent)
        parent._rules_win = rules_win
        rules_win.title("Правила игры")
        rules_win.geometry("1100x600")
        rules_win.configure(bg=HexUI.COLORS['background'])
        rules_win.resizable(False, False)

        content_frame = tk.Frame(rules_win, bg=HexUI.COLORS['background'])
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        rules_text = (
            "Правила игры:\n"
            "1) Игроки по очереди ставят фишки на гексагональную сетку: Черные и Белые(бот).\n"
            "2) Черные должны соединить ЛЕВЫЙ и ПРАВЫЙ края поля своей непрерывной цепочкой.\n"
            "3) Белые должны соединить ВЕРХНИЙ и НИЖНИЙ края поля своей непрерывной цепочкой.\n"
            "4) Побеждает тот, кто первым соединит свои стороны.\n"
            "5) Если поле заполнено без цепочки — ничья.\n"
        )
        tk.Label(content_frame, text=rules_text, font=HexUI.FONTS['rules'],
                 bg=HexUI.COLORS['background'], fg=HexUI.COLORS['text'],
                 justify=tk.LEFT).pack(pady=20, padx=20)
        HexUI.create_button(content_frame, text="Закрыть", command=rules_win.destroy,
                            bg=HexUI.COLORS['accent']).pack(pady=20)
        return rules_win
    @staticmethod
    def create_board_canvas(parent, size):
        return tk.Canvas(parent, bg=HexUI.COLORS['board'], highlightthickness=0)
    @staticmethod
    def draw_hexagon(canvas, x, y, size, fill='white'):
        pts = [
            x + size, y,
            x + size / 2, y + size * math.sqrt(3) / 2,
            x - size / 2, y + size * math.sqrt(3) / 2,
            x - size, y,
            x - size / 2, y - size * math.sqrt(3) / 2,
            x + size / 2, y - size * math.sqrt(3) / 2
        ]
        return canvas.create_polygon(pts, outline=HexUI.COLORS['hexagon'], fill=fill, width=2, smooth=True)
    @staticmethod
    def draw_piece(canvas, x, y, size, player):
        color = HexUI.COLORS['black_piece'] if player == 1 else HexUI.COLORS['white_piece']
        return canvas.create_oval(x - size, y - size, x + size, y + size,
                                  fill=color, outline=HexUI.COLORS['hexagon'], width=2)
    @staticmethod
    def create_control_panel(parent):
        return tk.Frame(parent, bg=HexUI.COLORS['background'], padx=10, pady=10)
    @staticmethod
    def create_status_label(parent):
        return tk.Label(parent, text="Ход игрока: Черные", font=HexUI.FONTS['status'],
                        bg=HexUI.COLORS['background'], fg=HexUI.COLORS['text'])

class HexGame:
    HEX_DIRS = [(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]
    def __init__(self, root, size=11, bot_difficulty="easy", main_menu_callback=None):
        self.root = root
        self.size = size
        self.bot_difficulty = self._normalize_diff(bot_difficulty)
        self.main_menu_callback = main_menu_callback
        self.window_width = 1920
        self.window_height = 1150
        self.canvas = HexUI.create_board_canvas(root, size)
        self.canvas.config(width=self.window_width, height=self.window_height)
        self.canvas.pack()
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1
        self.bot_player = 2
        self.hex_size = 35
        self.adjust_hex_size()
        self.game_over = False
        self.control_frame = HexUI.create_control_panel(root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=3)
        self.status_label = HexUI.create_status_label(self.control_frame)
        self.status_label.config(text=f"Ход игрока: Черные | Доска: {self.size}x{self.size} | Бот: {self._diff_ru(self.bot_difficulty)}")
        self.status_label.pack(side=tk.LEFT, padx=10)
        HexUI.create_button(self.control_frame, text="Правила игры", command=self.show_rules,
                            font=HexUI.FONTS['button_small']).pack(side=tk.LEFT, padx=10)
        HexUI.create_button(self.control_frame, text="Перезапуск", command=self.restart_game,
                            font=HexUI.FONTS['button_small']).pack(side=tk.LEFT, padx=10)
        HexUI.create_button(self.control_frame, text="Выход", command=self.root.quit,
                            font=HexUI.FONTS['button_small'], bg=HexUI.COLORS['accent']).pack(side=tk.RIGHT, padx=10)
        HexUI.create_button(self.control_frame, text="В меню", command=self.back_to_menu,
                            font=HexUI.FONTS['button_small']).pack(side=tk.RIGHT, padx=10)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)
        self.last_human_move = None
        self.bot_turn_index = 0
        self.search_deadline = None

    def back_to_menu(self):
        self.canvas.destroy()
        self.control_frame.destroy()
        if self.main_menu_callback:
            self.main_menu_callback()

    def _normalize_diff(self, d):
        m = {'легкий':'easy','лёгкий':'easy','средний':'medium','сложный':'hard',
             'easy':'easy','medium':'medium','hard':'hard'}
        return m.get(str(d).lower(), 'easy')
    def _diff_ru(self, d):
        return {'easy':'Легкий','medium':'Средний','hard':'Сложный'}.get(d,'Легкий')

    def adjust_hex_size(self):
        if self.size == 11:
            self.hex_size = 35
        elif self.size == 13:
            self.hex_size = 30
        else:
            self.hex_size = 24

    def draw_board(self):
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.hex_to_pixel(r, c)
                HexUI.draw_hexagon(self.canvas, x, y, self.hex_size, fill=HexUI.COLORS['hexagon'])

    def hex_to_pixel(self, row, col):
        start_x = (self.window_width - (self.size * self.hex_size * 1.5)) / 2
        start_y = (self.window_height - (self.size * self.hex_size * math.sqrt(3))) / 2
        x = start_x + col * self.hex_size * 1.5
        y = start_y + row * self.hex_size * math.sqrt(3) + (col * self.hex_size * math.sqrt(3) / 2) - 100
        return x, y

    def click_event(self, event):
        if self.game_over:
            print("Игра окончена, ходы запрещены")
            return
        row, col = self.pixel_to_hex(event.x, event.y)
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            self.make_move(row, col, human=True)
            if not self.game_over and self.current_player == self.bot_player:
                self.root.after(100, self.bot_move)  # Увеличена задержка для стабильности

    def pixel_to_hex(self, x, y):
        closest_row, closest_col = 0, 0
        min_dist = float("inf")
        for row in range(self.size):
            for col in range(self.size):
                hx, hy = self.hex_to_pixel(row, col)
                d = (hx - x) ** 2 + (hy - y) ** 2
                if d < min_dist:
                    min_dist = d
                    closest_row, closest_col = row, col
        return closest_row, closest_col

    def place_piece(self, row, col):
        x, y = self.hex_to_pixel(row, col)
        HexUI.draw_piece(self.canvas, x, y, self.hex_size * 0.4, self.board[row][col])

    def get_neighbors(self, r, c):
        for dr, dc in HexGame.HEX_DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                yield nr, nc

    def check_win(self, player):
        n = self.size
        visited = [[False]*n for _ in range(n)]
        q = deque()
        if player == 1:
            for r in range(n):
                if self.board[r][0] == 1:
                    q.append((r, 0))
                    visited[r][0] = True
            while q:
                r, c = q.popleft()
                if c == n-1:
                    print(f"Победа игрока {player} (Черные): найдена цепочка от левого края до правого")
                    return True
                for nr, nc in self.get_neighbors(r, c):
                    if not visited[nr][nc] and self.board[nr][nc] == 1:
                        visited[nr][nc] = True
                        q.append((nr, nc))
        else:
            for c in range(n):
                if self.board[0][c] == 2:
                    q.append((0, c))
                    visited[0][c] = True
            while q:
                r, c = q.popleft()
                if r == n-1:
                    print(f"Победа игрока {player} (Белые): найдена цепочка от верхнего края до нижнего")
                    return True
                for nr, nc in self.get_neighbors(r, c):
                    if not visited[nr][nc] and self.board[nr][nc] == 2:
                        visited[nr][nc] = True
                        q.append((nr, nc))
        print(f"Проверка победы игрока {player}: цепочка не найдена")
        return False

    def board_full(self):
        is_full = all(self.board[r][c] != 0 for r in range(self.size) for c in range(self.size))
        if is_full:
            print("Доска полностью заполнена")
        return is_full

    def restart_game(self):
        self.canvas.delete("all")
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1
        self.game_over = False
        self.last_human_move = None
        self.bot_turn_index = 0
        self.status_label.config(text=f"Ход игрока: Черные | Доска: {self.size}x{self.size} | Бот: {self._diff_ru(self.bot_difficulty)}")
        self.draw_board()

    def show_rules(self):
        HexUI.create_rules_window(self.root)

    def make_move(self, row, col, human=False):
        if self.game_over:
            print("Попытка сделать ход после окончания игры")
            return
        print(f"Ход: ({row}, {col}) игроком {self.current_player} {'(человек)' if human else '(бот)'}")
        self.board[row][col] = self.current_player
        self.place_piece(row, col)
        # Проверяем победу текущего игрока
        if self.check_win(self.current_player):
            self.game_over = True
            who = 'Черные' if self.current_player == 1 else 'Белые'
            self.status_label.config(text=f"Победа: {who} (соединена цепочка)!")
            self.root.after(100, lambda: tk.messagebox.showinfo("Игра окончена", f"Победа: {who}!\nСоединена цепочка."))
            return
        # Проверяем на ничью: доска заполнена, и никто не победил
        if self.board_full():
            black_wins = self.check_win(1)
            white_wins = self.check_win(2)
            if not black_wins and not white_wins:
                self.game_over = True
                self.status_label.config(text="Ничья: поле заполнено без победной цепочки!")
                self.root.after(100, lambda: tk.messagebox.showinfo("Игра окончена", "Ничья: поле заполнено, но ни один игрок не создал цепочку!"))
                return
        if human:
            self.last_human_move = (row, col)
        self.current_player = 3 - self.current_player
        self.status_label.config(text=f"Ход игрока: {'Черные' if self.current_player==1 else 'Белые'} | Доска: {self.size}x{self.size} | Бот: {self._diff_ru(self.bot_difficulty)}")

    def bot_move(self):
        if self.game_over or self.current_player != self.bot_player:
            print("Бот: игра окончена или не мой ход")
            return
        self.bot_turn_index += 1
        print(f"Ход бота (сложность: {self.bot_difficulty})")
        # Проверяем немедленный выигрыш
        mv = self.find_winning_move(self.bot_player)
        if mv:
            print(f"Бот: найден выигрышный ход {mv}")
            self.make_move(mv[0], mv[1], human=False)
            return
        # Проверяем, не надо ли блокировать игрока
        block = self.find_winning_move(3 - self.bot_player)
        if block:
            print(f"Бот: блокировка хода игрока {block}")
            self.make_move(block[0], block[1], human=False)
            return
        move = None
        if self.bot_difficulty == 'easy':
            ms = self.legal_moves()
            move = random.choice(ms) if ms else None

        elif self.bot_difficulty == 'medium':
            # Сначала ищем угрозу победы игрока
            danger = self.find_winning_move(3 - self.bot_player)
            if danger:
                move = danger
                print(f"Бот (medium): блокировка угрозы {move}")
            else:
                # Если нет угрозы — ходим около последнего хода игрока
                if self.last_human_move:
                    adj = self.adjacent_free(self.last_human_move[0], self.last_human_move[1])
                    if adj:
                        move = random.choice(adj)
                        print(f"Бот (medium): ход рядом с игроком {move}")
                # Если нет — применяем жадные эвристики
                if move is None:
                    move = self.greedy_tradeoff_move()
                    print(f"Бот (medium): жадный ход (tradeoff) {move}")
                if move is None:
                    move = self.greedy_reduce_own_distance()
                    print(f"Бот (medium): жадный ход (reduce distance) {move}")

        else:  # hard
            ms = self.candidate_moves()
            if not ms:
                ms = self.legal_moves()
            free_cells = len(self.legal_moves())
            depth_cap = 6 if self.size <= 11 else 5
            budget = 5.0  # до 5 секунд на ход
            if free_cells <= 25:
                depth_cap += 2
                budget += 3.0
            elif free_cells <= 40:
                depth_cap += 1
                budget += 2.0
            print(f"Бот (hard): свободных клеток = {free_cells}, глубина = {depth_cap}, время = {budget:.1f}с")
            self.search_deadline = time.time() + budget
            move = self.id_search(ms, depth_cap)
            print(f"Бот: ход после ID-поиска {move}")
            if move is None:
                move = self.greedy_tradeoff_move()
                print(f"Бот: жадный ход (tradeoff) {move}")
            if move is None:
                move = self.greedy_reduce_own_distance()
                print(f"Бот: жадный ход (reduce distance) {move}")
        if move is None:
            ms = self.legal_moves()
            move = random.choice(ms) if ms else None
            print(f"Бот: случайный ход {move}")
        if move is None:
            print("Бот: нет доступных ходов")
            self.current_player = 1
            self.status_label.config(
                text=f"Ход игрока: Черные | Доска: {self.size}x{self.size} | Бот: {self._diff_ru(self.bot_difficulty)}"
            )
            return
        r, c = move
        self.make_move(r, c, human=False)

    def legal_moves(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]

    def occupied(self):
        return [(r,c) for r in range(self.size) for c in range(self.size) if self.board[r][c] != 0]

    def candidate_moves(self):
        occ = self.occupied()
        if not occ:
            mid = (self.size // 2, self.size // 2)
            return [mid] if self.board[mid[0]][mid[1]] == 0 else self.legal_moves()
        seen = set()
        for r, c in occ:
            for dr, dc in HexGame.HEX_DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == 0:
                    seen.add((nr, nc))
        return list(seen) if seen else self.legal_moves()

    def adjacent_free(self, r, c):
        res = []
        for dr, dc in HexGame.HEX_DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == 0:
                res.append((nr, nc))
        return res

    def connection_distance(self, player):
        n = self.size
        INF = 10**9
        dist = [[INF]*n for _ in range(n)]
        pq = []

        def cell_cost(r, c):
            if self.board[r][c] == player:
                return 0
            elif self.board[r][c] == 0:
                return 1
            else:
                return INF
        if player == 1:
            for r in range(n):
                c = 0
                cost = cell_cost(r, c)
                if cost < INF:
                    dist[r][c] = cost
                    heapq.heappush(pq, (dist[r][c], r, c))
            target_col = n-1
            while pq:
                d, r, c = heapq.heappop(pq)
                if d != dist[r][c]:
                    continue
                if c == target_col:
                    return d
                for nr, nc in self.get_neighbors(r, c):
                    w = cell_cost(nr, nc)
                    nd = d + w
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heapq.heappush(pq, (nd, nr, nc))
        else:
            for c in range(n):
                r = 0
                cost = cell_cost(r, c)
                if cost < INF:
                    dist[r][c] = cost
                    heapq.heappush(pq, (dist[r][c], r, c))
            target_row = n-1
            while pq:
                d, r, c = heapq.heappop(pq)
                if d != dist[r][c]:
                    continue
                if r == target_row:
                    return d
                for nr, nc in self.get_neighbors(r, c):
                    w = cell_cost(nr, nc)
                    nd = d + w
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heapq.heappush(pq, (nd, nr, nc))
        return INF

    def static_eval(self):
        """Улучшенная оценка позиции: приоритет - соединение своих сторон и блокировка соперника."""
        INF = 10 ** 9
        my = self.connection_distance(self.bot_player)
        op = self.connection_distance(3 - self.bot_player)
        if my >= INF: my = INF
        if op >= INF: op = INF
        score = (op - my) * 500.0

        # Бонус за количество "связанных" фишек (улучшает построение цепочки)
        def connectivity(player):
            total = 0
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == player:
                        for nr, nc in self.get_neighbors(r, c):
                            if self.board[nr][nc] == player:
                                total += 1
            return total

        score += connectivity(self.bot_player) * 10.0
        score -= connectivity(3 - self.bot_player) * 8.0

        return score

    def greedy_reduce_own_distance(self):
        """Выбираем ход, который максимально уменьшает расстояние бота (дельта),
        с небольшой подстраховкой — если ход ещё и ухудшает путь оппонента, это бонус."""
        best_score = -float('inf')
        best_move = None
        orig_my = self.connection_distance(self.bot_player)
        orig_op = self.connection_distance(3 - self.bot_player)

        for r, c in self.legal_moves():
            # пробуем ход
            self.board[r][c] = self.bot_player
            new_my = self.connection_distance(self.bot_player)
            new_op = self.connection_distance(3 - self.bot_player)
            self.board[r][c] = 0

            # дельты: положительная дельта — улучшение (уменьшение расстояния)
            my_delta = (orig_my - new_my)
            op_delta = (new_op - orig_op)  # положительное — делает оппоненту хуже

            # комбинируем: основной вес — my_delta, бонус — ухудшение оппонента
            score = my_delta * 1.0 + op_delta * 0.5

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def greedy_tradeoff_move(self):
        """Жадная эвристика: максимально ухудшить оппонента и/или улучшить себя — смотрим послеходовые дельты."""
        best = -float('inf')
        bm = None
        orig_my = self.connection_distance(self.bot_player)
        orig_op = self.connection_distance(3 - self.bot_player)

        for r, c in self.legal_moves():
            self.board[r][c] = self.bot_player
            my_new = self.connection_distance(self.bot_player)
            op_new = self.connection_distance(3 - self.bot_player)
            self.board[r][c] = 0

            my_delta = (orig_my - my_new)  # >0 — мы сократили свой путь
            op_delta = (op_new - orig_op)  # >0 — ухудшили оппонента

            # Формула: сильнее ценим ухудшение оппонента, но и своё улучшение важно
            score = (op_delta * 1.5) + (my_delta * 1.0)

            if score > best:
                best = score
                bm = (r, c)
        return bm

    def find_winning_move(self, player):
        for r, c in self.legal_moves():
            self.board[r][c] = player
            ok = self.check_win(player)
            self.board[r][c] = 0
            if ok:
                return (r, c)
        return None

    def id_search(self, moves, depth_cap):
        """Итеративный поиск с увеличенной глубиной и кэшем позиций."""
        self.ttable = {}  # кэш позиций: hash -> (depth, score)
        best_move = None
        ordered = self.move_order(moves, self.bot_player)

        for depth in range(1, depth_cap + 1):
            alpha, beta = -float('inf'), float('inf')
            local_best = None
            local_score = -float('inf')

            for r, c in ordered:
                if self.search_deadline and time.time() > self.search_deadline:
                    break
                self.board[r][c] = self.bot_player
                score = -self.negamax(depth - 1, 3 - self.bot_player, -beta, -alpha)
                self.board[r][c] = 0

                if score > local_score:
                    local_score = score
                    local_best = (r, c)
                if score > alpha:
                    alpha = score

            if local_best:
                best_move = local_best
                # переносим лучший ход наверх для move ordering
                if best_move in ordered:
                    ordered.remove(best_move)
                    ordered.insert(0, best_move)

        return best_move

    def negamax(self, depth, player, alpha, beta):
        """Negamax с альфа-бета отсечением и кэшем."""
        if self.search_deadline and time.time() > self.search_deadline:
            return self.static_eval()
        if self.check_win(3 - player):
            return -1_000_000 + (5 - depth)
        if depth == 0 or self.board_full():
            return self.static_eval()

        # Хэш позиции
        state_key = tuple(tuple(row) for row in self.board)
        if state_key in self.ttable and self.ttable[state_key][0] >= depth:
            return self.ttable[state_key][1]

        moves = self.candidate_moves()
        if not moves:
            moves = self.legal_moves()
        moves = self.move_order(moves, player)

        best = -float('inf')
        for r, c in moves:
            self.board[r][c] = player
            val = -self.negamax(depth - 1, 3 - player, -beta, -alpha)
            self.board[r][c] = 0
            if val > best:
                best = val
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break

        self.ttable[state_key] = (depth, best)
        return best

    def move_order(self, moves, player):
        """Улучшенный порядок ходов: приоритет тем, что уменьшают дистанцию себе и увеличивают её сопернику."""
        scored = []
        my_before = self.connection_distance(player)
        op_before = self.connection_distance(3 - player)

        for r, c in moves:
            self.board[r][c] = player
            my_after = self.connection_distance(player)
            op_after = self.connection_distance(3 - player)
            self.board[r][c] = 0

            my_delta = (my_before - my_after)
            op_delta = (op_after - op_before)

            # Весим оппонента сильнее — нужно мешать
            score = my_delta * 200 + op_delta * 300

            # Бонус за центральные ходы
            cr, cc = (self.size - 1) / 2, (self.size - 1) / 2
            score -= (abs(r - cr) + abs(c - cc)) * 2

            # Бонус за ходы рядом с последним игрока (чтобы блокировать цепочку)
            if self.last_human_move and abs(self.last_human_move[0] - r) <= 1 and abs(self.last_human_move[1] - c) <= 1:
                score += 100

            scored.append((score, (r, c)))

        scored.sort(reverse=True)
        return [m for _, m in scored]

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.configure(bg=HexUI.COLORS['background'])
        self.menu_frame = HexUI.create_menu_frame(root)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label = HexUI.create_title_label(self.menu_frame, "Гекс")
        self.title_label.pack(pady=50)
        HexUI.create_button(self.menu_frame, text="Начать игру",
                            command=self.select_board_size, font=HexUI.FONTS['button_large'], width=20).pack(pady=20)
        HexUI.create_button(self.menu_frame, text="Правила игры",
                            command=self.show_rules, font=HexUI.FONTS['button_large'], width=20).pack(pady=20)
        HexUI.create_button(self.menu_frame, text="Выход", command=self.root.quit,
                            font=HexUI.FONTS['button_large'], bg=HexUI.COLORS['accent'], width=20).pack(pady=20)

    def select_board_size(self):
        self.menu_frame.destroy()
        self.size_frame = HexUI.create_menu_frame(self.root)
        self.size_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.size_frame, text="Выберите размер доски",
                 font=HexUI.FONTS['title'], bg=HexUI.COLORS['background'], fg=HexUI.COLORS['text']).pack(pady=50)
        sizes = [("11x11 (классический)", 11), ("13x13 (средний)", 13), ("19x19 (большой)", 19)]
        for text, size in sizes:
            HexUI.create_button(self.size_frame, text=text,
                                command=lambda s=size: self.select_difficulty(s),
                                font=HexUI.FONTS['button_medium'], width=25).pack(pady=10)
        HexUI.create_button(self.size_frame, text="Назад",
                            command=self.back_to_menu, font=HexUI.FONTS['button_small'], width=15).pack(pady=30)

    def select_difficulty(self, board_size):
        self.size_frame.destroy()
        self.difficulty_frame = HexUI.create_menu_frame(self.root)
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.difficulty_frame, text=f"Доска {board_size}x{board_size}\nВыберите уровень сложности",
                 font=HexUI.FONTS['title'], bg=HexUI.COLORS['background'], fg=HexUI.COLORS['text']).pack(pady=50)
        for diff in ["Легкий", "Средний", "Сложный"]:
            HexUI.create_button(self.difficulty_frame, text=diff,
                                command=lambda d=diff.lower(): self.start_hex_game(board_size, d),
                                font=HexUI.FONTS['button_medium'], width=20).pack(pady=15)
        HexUI.create_button(self.difficulty_frame, text="Назад",
                            command=lambda: self.back_to_size_select(board_size),
                            font=HexUI.FONTS['button_small'], width=15).pack(pady=30)

    def start_hex_game(self, board_size, difficulty):
        self.difficulty_frame.destroy()
        self.game = HexGame(self.root, size=board_size, bot_difficulty=difficulty, main_menu_callback=self.back_to_menu)

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def back_to_size_select(self, board_size):
        self.difficulty_frame.destroy()
        self.select_board_size()

    def show_rules(self):
        HexUI.create_rules_window(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()