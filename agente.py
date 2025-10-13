import numpy as np
from board import Board
from Node import Node, minimax


PLAYER_AGENT = 1   # peça da IA
PLAYER_HUMAN = 0   # peça do jogador humano
EMPTY = 2          # valor que representa casa vazia
N_ROWS, N_COLS = 4, 4


class Agente:
    def __init__(self):
        pass

    """
    Gera todos os possíveis tabuleiros após uma jogada do jogador atual.

    @:param board (Board): Estado atual do tabuleiro.
    @:param curr_player (int): Jogador que fará a jogada (PLAYER_AGENT ou PLAYER_HUMAN).    
        
    @:return list[tuple[int, Board, bool]]: Uma lista de tuplas (coluna, novo_board, venceu?).
    """

    def generate_children(self, board: Board, curr_player: int):
        children = []

        for col in range(N_COLS):
            new_board = board.copy()
            ok, row = new_board.add_chip(col, curr_player)

            if ok:
                # Usa o solver() do Board para verificar se a jogada levou à vitória
                win = new_board.solver(curr_player, row, col)
                children.append((col, new_board, win))

        return children

    """
            Constrói recursivamente uma árvore de Nodes a partir do tabuleiro.

            @:param board (Board): Tabuleiro atual.                
            @:param curr_player (int): Jogador que fará a próxima jogada.

            @:return Node: Raiz da subárvore correspondente a esse estado do jogo.
    """

    def board_to_node(self, board: Board, curr_player: int, depth=0, max_depth=4) -> Node:
        rows, cols = board.board.shape

        # 1️⃣ Limite de profundidade (evita explosão combinatória)
        if depth >= max_depth:
            return Node(utility=0)

        # 2️⃣ Verifica estados terminais (vitória)
        for i in range(rows):
            for j in range(cols):
                piece = board.board[i][j]
                if piece == PLAYER_AGENT and board.solver(PLAYER_AGENT, i, j):
                    return Node(utility=1)
                if piece == PLAYER_HUMAN and board.solver(PLAYER_HUMAN, i, j):
                    return Node(utility=-1)

        # 3️⃣ Empate
        if np.all(board.top_row() != EMPTY):
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

    def choose_move(self, board: Board) -> int:
        best_val = -np.inf
        best_col = None

        max_depth = 8

        for col, child_board, win in self.generate_children(board, PLAYER_AGENT):
            if win:
                return col  # vitória imediata

            node = self.board_to_node(child_board, PLAYER_HUMAN, depth=0, max_depth=max_depth)
            val = minimax(node)

            if val > best_val:
                best_val = val
                best_col = col

        return -1 if best_col is None else best_col
