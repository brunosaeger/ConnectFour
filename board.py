import numpy as np

class Board:
    def __init__(self, rows=6, cols=7, connect=4):
        self.rows = rows
        self.cols = cols
        self.connect = connect
        self.board = np.array([[2 for _ in range(cols)] for _ in range(rows)])

    def add_chip(self, column, curr_player):
        if self.board[0][column] != 2:
            return (False, 0)

        for i in range(self.rows - 1, -1, -1):
            if self.board[i][column] == 2:
                self.board[i][column] = curr_player
                return (True, i)
        return (False, 0)

    def top_row(self):
        return self.board[0]

    def solver(self, player, i, j):
        num_rows, num_cols = self.board.shape

        # ---- horizontal ----
        l = j
        r = j
        while l > 0 and self.board[i][l - 1] == player:
            l -= 1
        while r < num_cols - 1 and self.board[i][r + 1] == player:
            r += 1
        if r - l + 1 >= 4:
            return True

        # ---- vertical ----
        t = i
        b = i
        while t > 0 and self.board[t - 1][j] == player:
            t -= 1
        while b < num_rows - 1 and self.board[b + 1][j] == player:
            b += 1
        if b - t + 1 >= 4:
            return True

        return False

    def copy(self):
        new_board = Board(self.rows, self.cols)
        new_board.board = self.board.copy()
        return new_board

    def __str__(self):
        return str(self.board)
