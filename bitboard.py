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
        if self.canPlay(column):
            if not self.solver(column):
                self.changePlayer()
                # Adiciona peça
                self.mask |= self.mask + self.bottom_mask(column)
                self.moves += 1

            return True
        
        return False

    def draw(self):
        return self.mask & Bitboard.TOP_MASK == Bitboard.TOP_MASK
    
    def playable_columns(self):
        l = []

        for i in range(Bitboard.WIDTH):
            if self.mask & self.top_mask(i) == 0:
                l.append(i)

        return l

    def solver(self, col, verbose=False):
        pos = self.curr_position
        pos |= (self.mask + self.bottom_mask(col)) & self.column_mask(col)
        print(pos)
        return self.alignment(pos, verbose)

    def alignment(self, pos, verbose):
        # Horizontal 
        m = pos & (pos >> (Bitboard.HEIGHT+1))
        if(m & (m >> (2*(Bitboard.HEIGHT+1)))):
            if verbose:
                print("H")
            return True

        # Diagonal 1
        m = pos & (pos >> Bitboard.HEIGHT)
        if(m & (m >> (2*Bitboard.HEIGHT))):
            if verbose:
                print("D1")
            return True

        # Diagonal 2 
        m = pos & (pos >> (Bitboard.HEIGHT+2))
        if(m & (m >> (2*(Bitboard.HEIGHT+2)))):
            if verbose:
                print("D2")
            return True

        # Vertical;
        m = pos & (pos >> 1)
        if(m & (m >> 2)):
            if verbose:
                print("V")
            return True

        return False
    
    def possible(self):
        return (self.mask + Bitboard.BOTTOM_MASK) & Bitboard.BOARD_MASK

    def winning_positions(self, pos, mask):
        """
        Retorna um binário com todas as posições em que uma jogada causará a vitória
        """

        # Vertical
        r = (pos << 1) & (pos << 2) & (pos << 3)

        # Horizontal
        p = (pos << (Bitboard.HEIGHT+1)) & (pos << 2*(Bitboard.HEIGHT+1))
        r |= p & (pos << 3*(Bitboard.HEIGHT+1))
        r |= p & (pos >> (Bitboard.HEIGHT+1))
        p >>= 3*(Bitboard.HEIGHT+1)
        r |= p & (pos << (Bitboard.HEIGHT+1))
        r |= p & (pos >> 3*(Bitboard.HEIGHT+1))

        # Diagonal Primária
        p = (pos << Bitboard.HEIGHT) & (pos << 2*Bitboard.HEIGHT)
        r |= p & (pos << 3*Bitboard.HEIGHT)
        r |= p & (pos >> Bitboard.HEIGHT)
        p >>= 3*Bitboard.HEIGHT
        r |= p & (pos << Bitboard.HEIGHT)
        r |= p & (pos >> 3*Bitboard.HEIGHT)

        # Diagonal Secundária
        p = (pos << (Bitboard.HEIGHT+2)) & (pos << 2*(Bitboard.HEIGHT+2))
        r |= p & (pos << 3*(Bitboard.HEIGHT+2))
        r |= p & (pos >> (Bitboard.HEIGHT+2))
        p >>= 3*(Bitboard.HEIGHT+2)
        r |= p & (pos << (Bitboard.HEIGHT+2))
        r |= p & (pos >> 3*(Bitboard.HEIGHT+2))

        return r & (Bitboard.BOARD_MASK ^ mask)

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
        return str(self.board)

    def key(self):
        return self.curr_position + self.mask