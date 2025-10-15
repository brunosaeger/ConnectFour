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
    
    def top_rows_mask(self, rows):
        return Bitboard.BOARD_MASK ^ self.bottom_rows_mask(Bitboard.HEIGHT - rows)

    def bottom_mask(self, col):
        return 1 << col * Bitboard.HEIGHT
    
    def bottom_rows_mask(self, rows):
        return ((1 << rows) - 1) * Bitboard.BOTTOM_MASK

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
        m &= self.top_rows_mask(3)

        if m:
            return True

        # Diagonal 2
        m = pos & (pos >> (Bitboard.HEIGHT+1))
        m &= (m >> (2*(Bitboard.HEIGHT+1)))
        m &= self.bottom_rows_mask(3)

        if m:
            return True

        # Vertical;
        m = pos & (pos >> 1)
        m &= (m >> 2)
        m &= self.bottom_rows_mask(3)

        if m:
            return True

        return False

    def possibleWins(self):
        # Máscara com espaços livres e espaços do jogador
        pos = (self.mask ^ Bitboard.BOARD_MASK) | self.curr_position
        return self.possibleConnects(pos)
        
    def possibleConnects(self, pos, connect=4):
        shifts = connect-1
        wins = 0

        # Horizontal
        m = pos
        for _ in range(shifts):
            m &= (m >> (Bitboard.HEIGHT))

        wins += m.bit_count()

        # Diagonal 1
        m = pos
        for _ in range(shifts):
            m &= (m >> 5)

        m &= self.top_rows_mask(shifts)
        
        wins += m.bit_count()

        # Diagonal 2
        m = pos
        for _ in range(shifts):
            m &= (m >> (Bitboard.HEIGHT+1))

        m &= self.bottom_rows_mask(Bitboard.HEIGHT - shifts)

        wins += m.bit_count()

        # Vertical
        m = pos
        for _ in range(shifts):
            m &= (m >> 1)

        m &= self.bottom_rows_mask(Bitboard.HEIGHT - shifts)

        wins += m.bit_count()

        return wins

    def intermediate_heur(self):
        weights = [1, 10, 100]
        values = self.partialSequences()

        values[1] *= weights[1]
        values[2] *= weights[2]

        return sum(values)

    def partialSequences(self):
        values = [0, 0, 0]

        for i in range(3):
            values[i] = self.possibleConnects(self.curr_position, connect=i+1)
        
        values[1] -= values[2] * 2
        values[0] -= values[1] * 2
        values[0] -= values[2] * 3

        return values

    def adv_heur(self):
        weights = [1, 10, 100]
        values = self.partialSequencesBlock()

        values[1] *= weights[1]
        values[2] *= weights[2]

        return sum(values)

    def blockings(self):
        op_board = self.curr_position ^ self.mask
        cont = 0
        blocks = [0, 0, 0]

        for i in range(Bitboard.WIDTH * Bitboard.HEIGHT):
            mask = (1 << i)

            if self.curr_position & mask:
                cont += 1

                if op_board & (1 << (i+1)):
                    blocks[cont-1] += 1
            else:
                cont = 0
        
        return blocks

    def partialSequencesBlock(self):
        seq = self.partialSequences()
        blocks = self.blockings()

        return [seq[i] - blocks[i] for i in range(len(seq))]

    def centrality(self, curr_pos=None, mask=None):
        if curr_pos is None:
            curr_pos = self.curr_position
        if mask is None:
            mask = self.mask

        weights = [1, 5, 1, 10, 1, 5, 1]
        value = 0
        pos = (mask ^ Bitboard.BOARD_MASK) | curr_pos

        for i in range(len(weights)):
            m = pos & self.column_mask(i)
            value += m.bit_count() * weights[i]

        return value

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