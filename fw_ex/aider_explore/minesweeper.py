import random

class Minesweeper:
    def __init__(self, size=5, mines=5):
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.revealed = [[' ' for _ in range(size)] for _ in range(size)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.board[x][y] != 'M':
                self.board[x][y] = 'M'
                mines_placed += 1

    def calculate_numbers(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 'M':
                    continue
                count = 0
                for i in range(max(0, x-1), min(self.size, x+2)):
                    for j in range(max(0, y-1), min(self.size, y+2)):
                        if self.board[i][j] == 'M':
                            count += 1
                self.board[x][y] = str(count)

    def reveal(self, x, y):
        if self.board[x][y] == 'M':
            return False
        self.revealed[x][y] = self.board[x][y]
        return True

    def display(self):
        for row in self.revealed:
            print(' '.join(row))
        print()

    def play(self):
        while True:
            self.display()
            try:
                x, y = map(int, input("Enter coordinates to reveal (x y): ").replace(',', ' ').split())
                if x < 0 or x >= self.size or y < 0 or y >= self.size:
                    print("Invalid coordinates. Please enter values between 0 and", self.size - 1)
                    continue
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")
                continue
            if not self.reveal(x, y):
                print("Game Over! You hit a mine.")
                break
            if all(self.revealed[x][y] != ' ' for x in range(self.size) for y in range(self.size) if self.board[x][y] != 'M'):
                print("Congratulations! You've cleared the board.")
                break

if __name__ == "__main__":
    game = Minesweeper()
    game.play()
