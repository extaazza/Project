import tkinter as tk
import math

class HexGame:
    def __init__(self, root, size=11, bot_difficulty="easy"):
        self.root = root
        self.size = size
        self.bot_difficulty = bot_difficulty
        self.window_width = 1920
        self.window_height = 1150
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg="lightyellow")
        self.canvas.pack()
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1
        self.hex_size = 35  # Базовый размер шестиугольников
        self.adjust_hex_size()  # Подгоняем размер под выбранную доску
        self.game_over = False

        # Панель управления
        self.control_frame = tk.Frame(root, bg="lightgray")
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.status_label = tk.Label(self.control_frame,
                                   text=f"Ход игрока: Черные | Доска: {size}x{size}",
                                   font=("Arial", 14), bg="lightgray")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.rules_button = tk.Button(self.control_frame, text="Правила игры",
                                    font=("Arial", 12), command=self.show_rules)
        self.rules_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.control_frame, text="Перезапуск",
                                      font=("Arial", 12), command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.control_frame, text="Выход",
                                   font=("Arial", 12), command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)

    def adjust_hex_size(self):
        """Автоматическая подстройка размера гексов под размер доски"""
        if self.size == 11:
            self.hex_size = 35
        elif self.size == 13:
            self.hex_size = 30
        else:  # 19x19
            self.hex_size = 20

    def draw_board(self):
        for row in range(self.size):
            for col in range(self.size):
                x, y = self.hex_to_pixel(row, col)
                self.draw_hex(x, y)

    def draw_hex(self, x, y):
        size = self.hex_size
        points = [
            (x + size, y),
            (x + size / 2, y + size * math.sqrt(3) / 2),
            (x - size / 2, y + size * math.sqrt(3) / 2),
            (x - size, y),
            (x - size / 2, y - size * math.sqrt(3) / 2),
            (x + size / 2, y - size * math.sqrt(3) / 2)
        ]
        self.canvas.create_polygon(points, outline="black", fill="white", width=2)

    def hex_to_pixel(self, row, col):
        # Вычисляем начальные координаты для центрирования поля
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
            else:
                self.current_player = 3 - self.current_player
                self.status_label.config(text=f"Ход игрока: {'Черные' if self.current_player == 1 else 'Белые'} | Доска: {self.size}x{self.size}")

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
        color = "black" if self.current_player == 1 else "white"
        radius = max(10, self.hex_size * 0.4)  # Автоматический расчет радиуса фишки
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                              fill=color, outline="black")

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
        self.current_player = 1
        self.game_over = False
        self.status_label.config(text=f"Ход игрока: Черные | Доска: {self.size}x{self.size}")
        self.draw_board()

    def show_rules(self):
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("800x600")
        rules_window.configure(bg="lightyellow")

        rules_text = f"""
        Правила игры Гекс:

        1. Игра ведется на гексагональной доске размером {self.size}x{self.size}.
        2. Игроки по очереди размещают фишки своего цвета (черные или белые) на свободных ячейках.
        3. Цель игры — соединить противоположные стороны доски своими фишками:
           - Черные фишки должны соединить левую и правую стороны.
           - Белые фишки должны соединить верхнюю и нижнюю стороны.
        4. Первый ход может быть сделан в любую свободную ячейку.
        5. Ничья невозможна — всегда есть победитель.
        6. Игра заканчивается, когда один из игроков достигает своей цели.
        """

        rules_label = tk.Label(rules_window, text=rules_text,
                             font=("Arial", 14), bg="lightyellow", justify=tk.LEFT)
        rules_label.pack(pady=20, padx=20)

        exit_button = tk.Button(rules_window, text="Закрыть",
                              font=("Arial", 14), command=rules_window.destroy)
        exit_button.pack(pady=20)

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)

        self.menu_frame = tk.Frame(root, bg="lightyellow")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.menu_frame, text="Игра Гекс",
                                  font=("Arial", 48), bg="lightyellow")
        self.title_label.pack(pady=50)

        self.start_button = tk.Button(self.menu_frame, text="Начать игру",
                                    font=("Arial", 24), command=self.select_board_size)
        self.start_button.pack(pady=20)

        self.rules_button = tk.Button(self.menu_frame, text="Правила игры",
                                    font=("Arial", 24), command=self.show_rules)
        self.rules_button.pack(pady=20)

        self.exit_button = tk.Button(self.menu_frame, text="Выход",
                                   font=("Arial", 24), command=self.root.quit)
        self.exit_button.pack(pady=20)

    def select_board_size(self):
        """Окно выбора размера доски"""
        self.menu_frame.destroy()
        self.size_frame = tk.Frame(self.root, bg="lightyellow")
        self.size_frame.pack(fill=tk.BOTH, expand=True)

        self.size_label = tk.Label(self.size_frame,
                                 text="Выберите размер доски",
                                 font=("Arial", 36), bg="lightyellow")
        self.size_label.pack(pady=50)

        sizes = [("11x11 (классический)", 11),
                ("13x13 (средний)", 13),
                ("19x19 (большой)", 19)]

        for text, size in sizes:
            button = tk.Button(self.size_frame, text=text, font=("Arial", 24),
                             command=lambda s=size: self.select_difficulty(s))
            button.pack(pady=10)

        back_button = tk.Button(self.size_frame, text="Назад",
                              font=("Arial", 18), command=self.back_to_menu)
        back_button.pack(pady=30)

    def select_difficulty(self, board_size):
        """Окно выбора уровня сложности"""
        self.size_frame.destroy()
        self.difficulty_frame = tk.Frame(self.root, bg="lightyellow")
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)

        self.difficulty_label = tk.Label(self.difficulty_frame,
                                       text=f"Доска {board_size}x{board_size}\nВыберите уровень сложности",
                                       font=("Arial", 36), bg="lightyellow")
        self.difficulty_label.pack(pady=50)

        difficulties = ["Легкий", "Средний", "Сложный"]

        for diff in difficulties:
            button = tk.Button(self.difficulty_frame, text=diff, font=("Arial", 24),
                             command=lambda d=diff.lower(): self.start_hex_game(board_size, d))
            button.pack(pady=15)

        back_button = tk.Button(self.difficulty_frame, text="Назад",
                              font=("Arial", 18),
                              command=lambda: self.back_to_size_select(board_size))
        back_button.pack(pady=30)

    def start_hex_game(self, board_size, difficulty):
        """Запуск игры с выбранными параметрами"""
        self.difficulty_frame.destroy()
        self.game = HexGame(self.root, size=board_size, bot_difficulty=difficulty)

    def back_to_menu(self):
        """Возврат в главное меню"""
        self.size_frame.destroy()
        self.__init__(self.root)

    def back_to_size_select(self, board_size):
        """Возврат к выбору размера доски"""
        self.difficulty_frame.destroy()
        self.select_board_size()

    def show_rules(self):
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("1200x600")
        rules_window.configure(bg="lightyellow")

        rules_text = """
        Правила игры Гекс:

        1. Игра ведется на гексагональной доске (размер можно выбрать).
        2. Игроки по очереди размещают фишки своего цвета (черные или белые) на свободных ячейках.
        3. Цель игры — соединить противоположные стороны доски своими фишками:
           - Черные фишки должны соединить левую и правую стороны.
           - Белые фишки должны соединить верхнюю и нижнюю стороны.
        4. Первый ход может быть сделан в любую свободную ячейку.
        5. Ничья невозможна — всегда есть победитель.
        6. Игра заканчивается, когда один из игроков достигает своей цели.

        Доступные размеры доски:
        - 11x11 (классический)
        - 13x13 (средний)
        - 19x19 (большой)
        """

        rules_label = tk.Label(rules_window, text=rules_text,
                             font=("Arial", 14), bg="lightyellow", justify=tk.LEFT)
        rules_label.pack(pady=20, padx=20)

        exit_button = tk.Button(rules_window, text="Закрыть",
                              font=("Arial", 14), command=rules_window.destroy)
        exit_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
