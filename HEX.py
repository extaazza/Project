import tkinter as tk
import math

class HexGame:
    def __init__(self, root, size=11):
        self.root = root
        self.size = size
        self.window_width = 1920
        self.window_height = 1200
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg="lightblue")
        self.canvas.pack()
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1
        self.hex_size = self.calculate_hex_size()  # Автоматически рассчитываем размер шестиугольников
        self.game_over = False

        # Панель управления
        self.control_frame = tk.Frame(root, bg="lightgray")
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.status_label = tk.Label(self.control_frame, text="Ход игрока: Черные", font=("Arial", 14), bg="lightgray")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.control_frame, text="Перезапуск", font=("Arial", 12), command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.control_frame, text="Выход", font=("Arial", 12), command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)

    def calculate_hex_size(self):
        # Рассчитываем размер шестиугольников, чтобы поле помещалось на экране
        max_hex_width = self.window_width / (self.size * 1.5 + 1)
        max_hex_height = (self.window_height - 100) / (self.size * math.sqrt(3) + 1)  # Учитываем место для панели управления
        return min(max_hex_width, max_hex_height)

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
        # Центрируем поле по горизонтали и вертикали
        start_x = (self.window_width - (self.size * self.hex_size * 1.5)) / 2
        start_y = (self.window_height - (self.size * self.hex_size * math.sqrt(3))) / 2 + 50  # Смещаем поле вниз, чтобы не перекрывало панель управления
        x = start_x + col * self.hex_size * 1.5
        y = start_y + row * self.hex_size * math.sqrt(3) + (col * self.hex_size * math.sqrt(3) / 2)
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
                self.status_label.config(text=f"Ход игрока: {'Черные' if self.current_player == 1 else 'Белые'}")

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
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, outline="black")

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
            return any(dfs(r + dr, c + dc) for dr, dc in directions if 0 <= r + dr < self.size and 0 <= c + dc < self.size and self.board[r + dr][c + dc] == player)

        if player == 1:
            return any(dfs(r, 0) for r in range(self.size) if self.board[r][0] == player)
        else:
            return any(dfs(0, c) for c in range(self.size) if self.board[0][c] == player)

    def restart_game(self):
        self.canvas.delete("all")
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1
        self.game_over = False
        self.status_label.config(text="Ход игрока: Черные")
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Игра Гекс")
    root.geometry("1920x1200")  # Устанавливаем размер окна
    game = HexGame(root)
    root.mainloop()
