import numpy as np

class Board():
    def __init__(self, board=np.array([[2 for _ in range(7)] for _ in range(6)])):
        self.board = board

    def add_chip(self, column, curr_player):
        if self.board[0][column] != 2:
            return (False, 0)
        
        for i in range(5, -1, -1):
            if self.board[i][column] == 2:
                self.board[i][column] = curr_player

                return (True, i)
    
    def top_row(self):
        return self.board[0]

    def solver(self, player, i, j):
        l = j
        r = j
        t = i
        b = i

        while l > 0:
            if self.board[i][l-1] == player:
                l -= 1
            else:
                break

        while r < 6:
            if self.board[i][r+1] == player:
                r += 1
            else:
                break

        if r-l+1 == 4:
            return True

        while t > 0:
            if self.board[t-1][j] == player:
                t -= 1
            else:
                break

        while b < 5:
            if self.board[b+1][j] == player:
                b += 1
            else:
                break
        
        if b-t+1 == 4:
            return True

        return False
    
    def copy(self):
        return Board(self.board.copy())
    
    def __str__(self):
        return self.board.__str__()