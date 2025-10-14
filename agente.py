import numpy as np
from bitboard import Bitboard
from Node import Node, minimax
import time


PLAYER_AGENT = 1   # peça da IA
PLAYER_HUMAN = 0   # peça do jogador humano
EMPTY = 2          # valor que representa casa vazia


class Agente:
    def __init__(self, rows, cols, max_depth):
        self.rows = rows
        self.cols = cols
        self.max_depth = max_depth

    """
    Gera todos os possíveis tabuleiros após uma jogada do jogador atual.

    @:param board (Board): Estado atual do tabuleiro.
    @:param curr_player (int): Jogador que fará a jogada (PLAYER_AGENT ou PLAYER_HUMAN).    
        
    @:return list[tuple[int, Board, bool]]: Uma lista de tuplas (coluna, novo_board, venceu?).
    """

    def generate_children(self, board: Bitboard, curr_player: int):
        children = []

        for col in board.playable_columns():
            new_board = board.copy()

            if new_board.add_chip(col):
                # Usa o solver() do Board para verificar se a jogada levou à vitória
                win = new_board.solver(col)
                children.append((col, new_board, win))

        return children

    """
            Constrói recursivamente uma árvore de Nodes a partir do tabuleiro.

            @:param board (Board): Tabuleiro atual.                
            @:param curr_player (int): Jogador que fará a próxima jogada.

            @:return Node: Raiz da subárvore correspondente a esse estado do jogo.
    """

    def board_to_node(self, board: Bitboard, curr_player: int, depth=0, max_depth=4) -> Node:

        # 1️⃣ Limite de profundidade (evita explosão combinatória)
        if depth >= max_depth:
            return Node(utility=0)

        # 2️⃣ Verifica estados terminais (vitória)
        for col in board.playable_columns():
            if curr_player == PLAYER_AGENT and board.solver(col):
                return Node(utility=1)
            if curr_player == PLAYER_HUMAN and board.solver(col):
                return Node(utility=-1)

        # 3️⃣ Empate
        if board.draw():
            return Node(utility=0)

        # 4️⃣ Expande recursivamente
        node = Node()

        next_player = PLAYER_HUMAN if curr_player == PLAYER_AGENT else PLAYER_AGENT
        for _, child_board, _ in self.generate_children(board, curr_player):
            child_node = self.board_to_node(child_board, next_player, depth + 1, max_depth)
            node.add_child(child_node)

        return node

    """
        Escolhe a melhor jogada para o agente com base no minimax puro.

        @:param board (Board): Estado atual do tabuleiro.
                

        @:return int: Coluna escolhida (0–6), ou -1 se não houver jogadas válidas.
    """

    def choose_move(self, board: Bitboard) -> int:
        best_val = -np.inf
        best_col = None

        for col, child_board, win in self.generate_children(board, PLAYER_AGENT):
            if win:
                return col  # vitória imediata

            node = self.board_to_node(child_board, PLAYER_HUMAN, 0, self.max_depth)
            val = minimax(node)

            if val > best_val:
                best_val = val
                best_col = col

        return -1 if best_col is None else best_col
    
    def board_to_node_time(self, board: Bitboard, curr_player: int, depth=0, max_depth=4) -> Node:

        # 1️⃣ Limite de profundidade (evita explosão combinatória)
        if depth >= max_depth:
            return Node(utility=0)

        # 2️⃣ Verifica estados terminais (vitória)
        for col in board.playable_columns():
            if curr_player == PLAYER_AGENT and board.solver(col):
                return Node(utility=1)
            if curr_player == PLAYER_HUMAN and board.solver(col):
                return Node(utility=-1)

        # 3️⃣ Empate
        if board.draw():
            return Node(utility=0)

        # 4️⃣ Expande recursivamente
        node = Node()

        next_player = PLAYER_HUMAN if curr_player == PLAYER_AGENT else PLAYER_AGENT
        for _, child_board, _ in self.generate_children(board, curr_player):
            child_node = self.board_to_node(child_board, next_player, depth + 1, max_depth)
            node.add_child(child_node)

        return node

    def choose_move_time(self, board: Bitboard, time_limit: float = 3.0):
        start = time.perf_counter()
        deadline = start + time_limit

        best_col = None
        best_val = -np.inf
        depth = 1

        while True:
            if time.perf_counter() >= deadline:
                break

            cur_best_col = None
            cur_best_val = -np.inf

            for col, child_board, win in self.generate_children(board, PLAYER_AGENT):
                if time.perf_counter() >= deadline:
                    break

                if win:
                    return col, 1_000_000_000 #vitoria forçada
                

                node = self.board_to_node(child_board, PLAYER_HUMAN, 0, np.inf)
                val = minimax(node)

                if val > cur_best_val:
                    cur_best_val = val
                    cur_best_col = col

            if cur_best_col is not None:
                best_col, best_val = cur_best_col, cur_best_val


            if best_val >= 1_000_000_000:
                break

            depth += 1

            if best_col is None:
                for col, _, _ in self.generate_children(board, PLAYER_AGENT):
                    best_col = col
                    best_val = 0
                    break

            return best_col, best_val
        
        