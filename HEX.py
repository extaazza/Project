import tkinter as tk
import math
import random
from tkinter import font as tkfont


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
    def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    @staticmethod
    def create_button(parent, text, command, font=None, bg=None, fg=None, width=15):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=font or HexUI.FONTS['button_medium'],
            bg=bg or HexUI.COLORS['primary'],
            fg=fg or HexUI.COLORS['text'],
            activebackground=HexUI.COLORS['accent'],
            activeforeground=HexUI.COLORS['text'],
            borderwidth=0,
            highlightthickness=0,
            width=width,
            relief='flat'
        )
        return btn

    @staticmethod
    def create_menu_frame(root):
        frame = tk.Frame(root, bg=HexUI.COLORS['background'])
        return frame

    @staticmethod
    def create_title_label(parent, text):
        label = tk.Label(
            parent,
            text=text,
            font=HexUI.FONTS['title'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text']
        )
        return label

    @staticmethod
    def create_rules_window(parent):
        rules_win = tk.Toplevel(parent)
        rules_win.title("Правила игры")
        rules_win.geometry("800x600")
        rules_win.configure(bg=HexUI.COLORS['background'])
        rules_win.resizable(False, False)

        content_frame = tk.Frame(rules_win, bg=HexUI.COLORS['background'])
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)

        rules_text = """
        Правила игры Гекс:

        1. Игра ведется на гексагональной доске
        2. Два игрока по очереди ставят фишки
        3. Черные соединяют левую и правую стороны
        4. Белые соединяют верхнюю и нижнюю стороны
        5. Первый ход - в любую свободную ячейку
        6. Ничья невозможна - всегда есть победитель
        """

        rules_label = tk.Label(
            content_frame,
            text=rules_text,
            font=HexUI.FONTS['rules'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text'],
            justify=tk.LEFT
        )
        rules_label.pack(pady=20, padx=20)

        close_btn = HexUI.create_button(
            content_frame,
            text="Закрыть",
            command=rules_win.destroy,
            bg=HexUI.COLORS['accent']
        )
        close_btn.pack(pady=20)

        return rules_win

    @staticmethod
    def create_board_canvas(parent, size):
        canvas = tk.Canvas(
            parent,
            bg=HexUI.COLORS['board'],
            highlightthickness=0
        )
        return canvas

    @staticmethod
    def draw_hexagon(canvas, x, y, size, fill='white'):
        points = [
            x + size, y,
            x + size / 2, y + size * math.sqrt(3) / 2,
            x - size / 2, y + size * math.sqrt(3) / 2,
            x - size, y,
            x - size / 2, y - size * math.sqrt(3) / 2,
            x + size / 2, y - size * math.sqrt(3) / 2
        ]
        return canvas.create_polygon(
            points,
            outline=HexUI.COLORS['hexagon'],
            fill=fill,
            width=2,
            smooth=True
        )

    @staticmethod
    def draw_piece(canvas, x, y, size, player):
        color = HexUI.COLORS['black_piece'] if player == 1 else HexUI.COLORS['white_piece']
        return canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=color,
            outline=HexUI.COLORS['hexagon'],
            width=2
        )

    @staticmethod
    def create_control_panel(parent):
        panel = tk.Frame(
            parent,
            bg=HexUI.COLORS['background'],
            padx=10,
            pady=10
        )
        return panel

    @staticmethod
    def create_status_label(parent):
        label = tk.Label(
            parent,
            text="Ход игрока: Черные",
            font=HexUI.FONTS['status'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text']
        )
        return label

    @staticmethod
    def create_result_window(parent, winner):
        result_win = tk.Toplevel(parent)
        result_win.title("Игра завершена")
        result_win.geometry("400x300")
        result_win.configure(bg=HexUI.COLORS['background'])
        result_win.resizable(False, False)

        content_frame = tk.Frame(result_win, bg=HexUI.COLORS['background'])
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)

        result_text = f"Победитель: {winner}!"

        result_label = tk.Label(
            content_frame,
            text=result_text,
            font=HexUI.FONTS['title'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text'],
            justify=tk.CENTER
        )
        result_label.pack(pady=40)

        button_frame = tk.Frame(content_frame, bg=HexUI.COLORS['background'])
        button_frame.pack(pady=20)

        restart_btn = HexUI.create_button(
            button_frame,
            text="Новая игра",
            command=lambda: [result_win.destroy(), parent.restart_game()],
            bg=HexUI.COLORS['primary']
        )
        restart_btn.pack(side=tk.LEFT, padx=10)

        menu_btn = HexUI.create_button(
            button_frame,
            text="Главное меню",
            command=lambda: [result_win.destroy(), parent.return_to_menu()],
            bg=HexUI.COLORS['secondary']
        )
        menu_btn.pack(side=tk.LEFT, padx=10)

        return result_win


class HexGame:
    def __init__(self, root, size=11, bot_difficulty="easy"):
        self.root = root
        self.size = size
        self.bot_difficulty = bot_difficulty
        self.window_width = 1920
        self.window_height = 1150

        # Используем стили из HexUI
        self.canvas = HexUI.create_board_canvas(root, size)
        self.canvas.config(width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1  # Всегда начинают черные (игрок)
        self.hex_size = 35
        self.adjust_hex_size()
        self.game_over = False

        # Панель управления с использованием стилей HexUI
        self.control_frame = HexUI.create_control_panel(root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=3)

        self.status_label = HexUI.create_status_label(self.control_frame)
        self.status_label.config(text=f"Ход игрока: Черные | Доска: {size}x{size}")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.rules_button = HexUI.create_button(
            self.control_frame,
            text="Правила игры",
            command=self.show_rules,
            font=HexUI.FONTS['button_small']
        )
        self.rules_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = HexUI.create_button(
            self.control_frame,
            text="Перезапуск",
            command=self.restart_game,
            font=HexUI.FONTS['button_small']
        )
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = HexUI.create_button(
            self.control_frame,
            text="Выход",
            command=self.root.quit,
            font=HexUI.FONTS['button_small'],
            bg=HexUI.COLORS['accent']
        )
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        # Добавляем кнопку возврата в меню
        self.menu_button = HexUI.create_button(
            self.control_frame,
            text="В меню",
            command=self.return_to_menu,
            font=HexUI.FONTS['button_small'],
            bg=HexUI.COLORS['secondary']
        )
        self.menu_button.pack(side=tk.RIGHT, padx=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)

    def adjust_hex_size(self):
        if self.size == 11:
            self.hex_size = 35
        elif self.size == 13:
            self.hex_size = 30
        else:
            self.hex_size = 20

    def draw_board(self):
        for row in range(self.size):
            for col in range(self.size):
                x, y = self.hex_to_pixel(row, col)
                HexUI.draw_hexagon(self.canvas, x, y, self.hex_size, fill=HexUI.COLORS['hexagon'])

    def hex_to_pixel(self, row, col):
        start_x = (self.window_width - (self.size * self.hex_size * 1.5)) / 2
        start_y = (self.window_height - (self.size * self.hex_size * math.sqrt(3))) / 2
        x = start_x + col * self.hex_size * 1.5
        y = start_y + row * self.hex_size * math.sqrt(3) + (col * self.hex_size * math.sqrt(3) / 2) - 100
        return x, y

    def click_event(self, event):
        if self.game_over:
            return
        row, col = self.pixel_to_hex(event.x, event.y)
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            self.place_piece(row, col)
            if self.check_win(self.current_player):
                self.game_over = True
                winner = "Черные" if self.current_player == 1 else "Белые"
                self.status_label.config(text=f"Победил игрок: {winner}!")
                self.show_win_message(winner)
            else:
                self.current_player = 3 - self.current_player
                player_text = "Черные" if self.current_player == 1 else "Белые"
                self.status_label.config(text=f"Ход игрока: {player_text} | Доска: {self.size}x{self.size}")
                if self.current_player == 2:  # Ход бота
                    self.root.after(500, self.bot_move)

    def pixel_to_hex(self, x, y):
        closest_row, closest_col = 0, 0
        min_dist = float("inf")
        for row in range(self.size):
            for col in range(self.size):
                hex_x, hex_y = self.hex_to_pixel(row, col)
                dist = (hex_x - x) ** 2 + (hex_y - y) ** 2
                if dist < min_dist:
                    min_dist = dist
                    closest_row, closest_col = row, col
        return closest_row, closest_col

    def place_piece(self, row, col):
        x, y = self.hex_to_pixel(row, col)
        HexUI.draw_piece(self.canvas, x, y, self.hex_size * 0.4, self.current_player)

    def check_win(self, player):
        visited = set()

        def dfs(r, c):
            if (r, c) in visited:
                return False
            if player == 1 and c == self.size - 1:
                return True
            if player == 2 and r == self.size - 1:
                return True
            visited.add((r, c))
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]
            return any(dfs(r + dr, c + dc) for dr, dc in directions
                       if 0 <= r + dr < self.size and 0 <= c + dc < self.size
                       and self.board[r + dr][c + dc] == player)

        if player == 1:
            return any(dfs(r, 0) for r in range(self.size) if self.board[r][0] == player)
        else:
            return any(dfs(0, c) for c in range(self.size) if self.board[0][c] == player)

    def restart_game(self):
        self.canvas.delete("all")
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1  # Всегда начинают черные
        self.game_over = False
        self.status_label.config(text=f"Ход игрока: Черные | Доска: {self.size}x{self.size}")
        self.draw_board()

    def show_rules(self):
        HexUI.create_rules_window(self.root)

    def bot_move(self):
        if self.game_over or self.current_player != 2:
            return

        empty_cells = [(r, c) for r in range(self.size)
                       for c in range(self.size) if self.board[r][c] == 0]

        if not empty_cells:
            return

        if self.bot_difficulty == "easy":
            row, col = self.easy_bot_move(empty_cells)
        elif self.bot_difficulty == "medium":
            row, col = self.medium_bot_move(empty_cells)
        else:  # hard
            row, col = self.hard_bot_move(empty_cells)

        self.make_move(row, col)

    def make_move(self, row, col):
        """Общая функция для совершения хода"""
        self.board[row][col] = self.current_player
        self.place_piece(row, col)

        if self.check_win(self.current_player):
            self.game_over = True
            winner = "Черные" if self.current_player == 1 else "Белые"
            self.status_label.config(text=f"Победил игрок: {winner}!")
            self.show_win_message(winner)
        else:
            self.current_player = 3 - self.current_player
            player_text = "Черные" if self.current_player == 1 else "Белые"
            self.status_label.config(text=f"Ход игрока: {player_text} | Доска: {self.size}x{self.size}")

    def easy_bot_move(self, empty_cells):
        """Случайный ход с приоритетом центра и краев"""
        center = self.size // 2
        center_cells = []
        edge_cells = []
        other_cells = []

        for r, c in empty_cells:
            dist_to_center = max(abs(r - center), abs(c - center))
            if dist_to_center <= 2:
                center_cells.append((r, c))
            elif r == 0 or r == self.size - 1 or c == 0 or c == self.size - 1:
                edge_cells.append((r, c))
            else:
                other_cells.append((r, c))

        if center_cells:
            return random.choice(center_cells)
        elif edge_cells:
            return random.choice(edge_cells)
        else:
            return random.choice(other_cells)

    def medium_bot_move(self, empty_cells):
        """Бот среднего уровня с улучшенной стратегией"""
        # 1. Проверить, может ли бот выиграть сразу
        for r, c in empty_cells:
            self.board[r][c] = 2
            if self.check_win(2):
                self.board[r][c] = 0
                return r, c
            self.board[r][c] = 0

        # 2. Проверить, может ли игрок выиграть следующим ходом
        for r, c in empty_cells:
            self.board[r][c] = 1
            if self.check_win(1):
                self.board[r][c] = 0
                return r, c
            self.board[r][c] = 0

        # 3. Выбрать лучший ход по стратегическим соображениям
        return self.strategic_move(empty_cells)

    def hard_bot_move(self, empty_cells):
        """Упрощенная версия для быстрой работы"""
        # 1. Проверить немедленный выигрыш
        for r, c in empty_cells:
            self.board[r][c] = 2
            if self.check_win(2):
                self.board[r][c] = 0
                return r, c
            self.board[r][c] = 0

        # 2. Проверить немедленную угрозу
        for r, c in empty_cells:
            self.board[r][c] = 1
            if self.check_win(1):
                self.board[r][c] = 0
                return r, c
            self.board[r][c] = 0

        # 3. Использовать стратегический выбор с более простой оценкой
        best_score = -float('inf')
        best_move = random.choice(empty_cells)

        for r, c in empty_cells:
            score = self.evaluate_cell_hard(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def evaluate_cell_hard(self, r, c):
        """Упрощенная оценка клетки для hard уровня"""
        score = 0

        # Бонус за соединение с другими своими фишками
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if self.board[nr][nc] == 2:
                    score += 5
                elif self.board[nr][nc] == 1:
                    score -= 2

        # Бонус за центральные клетки
        center = self.size // 2
        distance = max(abs(r - center), abs(c - center))
        score += (self.size - distance) * 0.7

        # Бонус за важные края (для белых - верх/низ)
        if r == 0 or r == self.size - 1:
            score += 3

        return score

    def return_to_menu(self):
        self.canvas.destroy()
        self.control_frame.destroy()
        MainMenu(self.root)

    def show_win_message(self, winner):
        HexUI.create_result_window(self, winner)


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

        self.start_button = HexUI.create_button(
            self.menu_frame,
            text="Начать игру",
            command=self.select_board_size,
            font=HexUI.FONTS['button_large'],
            width=20
        )
        self.start_button.pack(pady=20)

        self.rules_button = HexUI.create_button(
            self.menu_frame,
            text="Правила игры",
            command=self.show_rules,
            font=HexUI.FONTS['button_large'],
            width=20
        )
        self.rules_button.pack(pady=20)

        self.exit_button = HexUI.create_button(
            self.menu_frame,
            text="Выход",
            command=self.root.quit,
            font=HexUI.FONTS['button_large'],
            bg=HexUI.COLORS['accent'],
            width=20
        )
        self.exit_button.pack(pady=20)

    def select_board_size(self):
        self.menu_frame.destroy()
        self.size_frame = HexUI.create_menu_frame(self.root)
        self.size_frame.pack(fill=tk.BOTH, expand=True)

        self.size_label = tk.Label(
            self.size_frame,
            text="Выберите размер доски",
            font=HexUI.FONTS['title'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text']
        )
        self.size_label.pack(pady=50)

        sizes = [("11x11 (классический)", 11),
                 ("13x13 (средний)", 13),
                 ("19x19 (большой)", 19)]

        for text, size in sizes:
            button = HexUI.create_button(
                self.size_frame,
                text=text,
                command=lambda s=size: self.select_difficulty(s),
                font=HexUI.FONTS['button_medium'],
                width=25
            )
            button.pack(pady=10)

        back_button = HexUI.create_button(
            self.size_frame,
            text="Назад",
            command=self.back_to_menu,
            font=HexUI.FONTS['button_small'],
            width=15
        )
        back_button.pack(pady=30)

    def select_difficulty(self, board_size):
        self.size_frame.destroy()
        self.difficulty_frame = HexUI.create_menu_frame(self.root)
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)

        self.difficulty_label = tk.Label(
            self.difficulty_frame,
            text=f"Доска {board_size}x{board_size}\nВыберите уровень сложности",
            font=HexUI.FONTS['title'],
            bg=HexUI.COLORS['background'],
            fg=HexUI.COLORS['text']
        )
        self.difficulty_label.pack(pady=50)

        difficulties = ["Легкий", "Средний", "Сложный"]

        for diff in difficulties:
            button = HexUI.create_button(
                self.difficulty_frame,
                text=diff,
                command=lambda d=diff.lower(): self.start_hex_game(board_size, d),
                font=HexUI.FONTS['button_medium'],
                width=20
            )
            button.pack(pady=15)

        back_button = HexUI.create_button(
            self.difficulty_frame,
            text="Назад",
            command=lambda: self.back_to_size_select(board_size),
            font=HexUI.FONTS['button_small'],
            width=15
        )
        back_button.pack(pady=30)

    def start_hex_game(self, board_size, difficulty):
        self.difficulty_frame.destroy()
        self.game = HexGame(self.root, size=board_size, bot_difficulty=difficulty)

    def back_to_menu(self):
        self.size_frame.destroy()
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
