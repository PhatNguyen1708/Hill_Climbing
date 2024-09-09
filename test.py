import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class NQueens:
    def __init__(self, size):
        self.size = size
        self.board = [0] * self.size
        self.initialize_board()
        self.x=0

    def initialize_board(self):
        self.board = [random.randint(0, self.size - 1) for _ in range(self.size)]
        self.x=self.calculate_conflicts(self.board)

    def calculate_conflicts(self, board):
        conflicts = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self):
        neighbors = []
        for col in range(self.size):
            for row in range(self.size):
                if self.board[col] != row:
                    neighbor = list(self.board)
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors

    def hill_climbing(self):
        current_conflicts = self.calculate_conflicts(self.board)
        while True:
            neighbors = self.get_neighbors()
            neighbor_conflicts = [self.calculate_conflicts(neighbor) for neighbor in neighbors]
            min_conflict = min(neighbor_conflicts)
            if min_conflict >= current_conflicts:
                break
            current_conflicts = min_conflict
            self.board = neighbors[neighbor_conflicts.index(min_conflict)]
        return self.board, current_conflicts == 0

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("N Queens Problem - Hill Climbing")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.size_entry = tk.Entry(self.master)
        self.size_entry.pack()
        self.size_entry.insert(0, "8")

        display_button = tk.Button(self.master, text="Hiển thị bàn cờ", command=self.display_board)
        display_button.pack()

        solve_button = tk.Button(self.master, text="Giải bài toán", command=self.solve)
        solve_button.pack()

        self.queen_image = Image.open("queen.png")
        self.queen_image = self.queen_image.resize((50, 50))
        self.queen_photo = ImageTk.PhotoImage(self.queen_image)
        self.queens = None

        self.text = text = tk.Label(self.master,text=f"aosfojkas:")
        self.text.pack()

    def draw_board(self):
        self.text.destroy()
        self.canvas.delete("all")
        size = self.queens.size
        cell_size = min(400 // size, 400 // size)
        for i in range(size):
            for j in range(size):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(i * cell_size, j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, fill=color)
                if self.queens.board[j] == i:
                    self.canvas.create_image(i * cell_size + cell_size // 2, j * cell_size + cell_size // 2, image=self.queen_photo)
        self.text = text = tk.Label(self.master,text=f"aosfojkas: {self.queens.x}")
        self.text.pack()

    def display_board(self):
        try:
            size = int(self.size_entry.get())
            if size < 4:
                messagebox.showerror("Error", "Number of queens must be 4 or greater.")
                return
            self.queens = NQueens(size)
            self.draw_board()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def solve(self):
        if not self.queens:
            messagebox.showerror("Error", "Please display the board first.")
            return
        while True:
            solved_board, solved = self.queens.hill_climbing()
            self.draw_board()
            if solved:
                messagebox.showinfo("Kết quả", "Đã tìm thấy giải pháp.")
                break
            else:
                # Nếu không tìm được, khởi tạo lại bàn cờ ngẫu nhiên và thử lại
                self.queens.initialize_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
