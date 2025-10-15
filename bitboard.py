import numpy as np

class Bitboard:
    WIDTH = 7
    HEIGHT = 6
    BOTTOM_MASK = 0b000001000001000001000001000001000001000001
    TOP_MASK = 0b100000100000100000100000100000100000100000
    BOARD_MASK = BOTTOM_MASK * ((1 << HEIGHT) - 1)

    def __init__(self, rows=6, cols=7, curr_position=0, mask=0, moves=0):
        Bitboard.HEIGHT = rows
        Bitboard.WIDTH = cols
        self.curr_position = curr_position
        self.mask = mask
        self.moves = moves

    def top_mask(self, col):
        return (1 << (Bitboard.HEIGHT - 1)) << col * Bitboard.HEIGHT
    
    def bottom_mask(self, col):
        return 1 << col * Bitboard.HEIGHT
    
    def column_mask(self, col):
        return ((1 << Bitboard.HEIGHT) - 1) << col * Bitboard.HEIGHT
    
    def canPlay(self, col):
        return (self.mask & self.top_mask(col)) == 0

    def changePlayer(self):
        self.curr_position ^= self.mask

    def add_chip(self, column):
        self.changePlayer()
        # Adiciona peça
        self.mask |= self.mask + self.bottom_mask(column)
        self.moves += 1

    def draw(self):
        return self.mask & Bitboard.TOP_MASK == Bitboard.TOP_MASK
    
    def playable_columns(self):
        l = []

        for i in range(Bitboard.WIDTH):
            if self.mask & self.top_mask(i) == 0:
                l.append(i)

        return l

    def solver(self, col):
        pos = self.curr_position
        pos |= (self.mask + self.bottom_mask(col)) & self.column_mask(col)
        return self.alignment(pos)

    def alignment(self, pos):
        # Horizontal 
        m = pos & (pos >> (Bitboard.HEIGHT))
        m &= (m >> (Bitboard.HEIGHT * 2))

        if m:
            return True

        # Diagonal 1
        m = pos & (pos >> 5)
        m &= (m >> 10)
        m &= 0b111000111000111000111000111000111000111000

        if m:
            return True

        # Diagonal 2
        m = pos & (pos >> (Bitboard.HEIGHT+1))
        m &= (m >> (2*(Bitboard.HEIGHT+1)))
        m &= 0b000111000111000111000111000111000111000111

        if m:
            return True

        # Vertical;
        m = pos & (pos >> 1)
        m &= (m >> 2)
        m &= 0b000111000111000111000111000111000111000111

        if m:
            return True

        return False

    def possibleWins(self):
        wins = 0
        pos = (self.mask ^ Bitboard.BOARD_MASK) | self.curr_position

        # Horizontal
        m = pos & (pos >> (Bitboard.HEIGHT))
        m &= (m >> (Bitboard.HEIGHT * 2))

        wins += m.bit_count()

        # Diagonal 1
        m = pos & (pos >> 5)
        m &= (m >> 10)
        m &= 0b111000111000111000111000111000111000111000
        
        wins += m.bit_count()

        # Diagonal 2
        #m = pos & 0b111000111100111110111111011111001111000111
        m = pos & (pos >> (Bitboard.HEIGHT+1))
        m &= (m >> (2*(Bitboard.HEIGHT+1)))
        m &= 0b000111000111000111000111000111000111000111

        wins += m.bit_count()

        # Vertical;
        m = pos & (pos >> 1)
        m &= (m >> 2)
        m &= 0b000111000111000111000111000111000111000111

        wins += m.bit_count()

        return wins

    def toMatrix(self):
        array = np.array([], dtype=int)
        curr_pos = self.curr_position
        mask = self.mask

        for i in range(Bitboard.HEIGHT-1, -1, -1):
            for j in range(Bitboard.WIDTH):
                if (mask >> (i + j*(Bitboard.HEIGHT))) & 1 == 0:
                    array = np.append(array, 2)
                else:
                    if (curr_pos >> (i + j*(Bitboard.HEIGHT))) & 1 == 1:
                        array = np.append(array, 0)
                    else:
                        array = np.append(array, 1)

        return array.reshape((Bitboard.HEIGHT, Bitboard.WIDTH))

    def copy(self):
        return Bitboard(curr_position=self.curr_position, mask=self.mask, moves=self.moves)

    def __str__(self):
        return self.toMatrix().__str__()

    def key(self):
        return self.curr_position + self.mask