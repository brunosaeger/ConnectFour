import numpy as np

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.array([[2 for _ in range(cols)] for _ in range(rows)])
    
    def getBoard(self):
        return self.board

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
        # Horizontal

        l = j
        r = j

        while l > 0:
            if self.board[i][l-1] == player:
                l -= 1
            else:
                break

        while r < self.cols-1:
            if self.board[i][r+1] == player:
                r += 1
            else:
                break

        if r-l+1 == 4:
            return True

        # Vertical

        t = i
        b = i

        while t > 0:
            if self.board[t-1][j] == player:
                t -= 1
            else:
                break

        while b < self.rows-1:
            if self.board[b+1][j] == player:
                b += 1
            else:
                break
        
        if b-t+1 == 4:
            return True
        
        # Diagonal principal

        d1l = [i, j]
        d1r = [i, j]

        while d1l[0] > 0 and d1l[1] > 0:
            if self.board[d1l[0]-1, d1l[1]-1] == player:
                d1l = [d1l[0]-1, d1l[1]-1]
            else:
                break

        while d1r[0] < self.rows-1 and d1r[1] < self.cols-1:
            if self.board[d1r[0]+1, d1r[1]+1] == player:
                d1r = [d1r[0]+1, d1r[1]+1]
            else:
                break

        if d1r[1]-d1l[1]+1 == 4:
            return True
        
        # Diagonal secundária

        d2l = [i, j]
        d2r = [i, j]

        while d2l[0] < self.rows-1 and d2l[1] > 0:
            if self.board[d2l[0]+1, d2l[1]-1] == player:
                d2l = [d2l[0]+1, d2l[1]-1]
            else:
                break

        while d2r[0] > 0 and d2r[1] < self.cols-1:
            if self.board[d2r[0]-1, d2r[1]+1] == player:
                d2r = [d2r[0]-1, d2r[1]+1]
            else:
                break

        if d2r[1]-d2l[1]+1 == 4:
            return True

        return False
    """
    def copy(self):
        new_board = Board(self.rows, self.cols)
        new_board.board = self.board.copy()
        return new_board
    """
    def __str__(self):
        return str(self.board)
