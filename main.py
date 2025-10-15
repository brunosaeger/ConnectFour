import pygame
from sys import exit

from agente import Agente, PLAYER_AGENT, PLAYER_HUMAN
from bitboard import Bitboard

if __name__ == "__main__":
    WIDTH = 700
    HEIGHT = 800
    CHIP_SIZE = 100

    N_ROWS = 6
    N_COLS = 7

    tabuleiro = Bitboard(N_ROWS, N_COLS)

    chip_enum = ["Red", "Yellow", "Blue"]

    curr_player = 0
    game_start = True
    game_ended = False
    difficulty = None

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24)

    start_time = 0
    tempo = [0, 0]
    aval = 0

    agent = Agente(N_ROWS, N_COLS, 3)

    # Tela Inicial

    while game_start:
        b1 = pygame.Rect(0, 0, 500, 100)
        b1.center = (WIDTH/2, 200)
        b2 = pygame.Rect(0, 0, 500, 100)
        b2.center = (WIDTH/2, 400)
        b3 = pygame.Rect(0, 0, 500, 100)
        b3.center = (WIDTH/2, 600)

        pygame.draw.rect(screen, "Blue", b1)
        b1_text = font.render("Iniciante", True, "Black")
        screen.blit(b1_text, (b1.centerx-b1_text.get_rect().width/2, b1.centery-b1_text.get_rect().height/2))

        pygame.draw.rect(screen, "Blue", b2)
        b2_text = font.render("Intermediário", True, "Black")
        screen.blit(b2_text, (b2.centerx-b2_text.get_rect().width/2, b2.centery-b2_text.get_rect().height/2))

        pygame.draw.rect(screen, "Blue", b3)
        b3_text = font.render("Profissional", True, "Black")
        screen.blit(b3_text, (b3.centerx-b3_text.get_rect().width/2, b3.centery-b3_text.get_rect().height/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(event.pos):
                    difficulty = 0
                    game_start = False
                elif b2.collidepoint(event.pos):
                    difficulty = 1
                    game_start = False
                elif b3.collidepoint(event.pos):
                    difficulty = 2
                    game_start = False

        pygame.display.update()
        clock.tick(30)

    # Tela de Jogo

    while not game_ended:
        mouse_pos = pygame.mouse.get_pos()
        column = mouse_pos[0] // CHIP_SIZE

        # Placar Humano
        pygame.draw.rect(screen, chip_enum[0], pygame.Rect(0, 0, WIDTH/2, 100))
        screen.blit(font.render("Agente Humano", True, "Black"), (0, 0))
        screen.blit(font.render(f"Última Jogada: {tempo[0]:.2f} s", True, "Black"), (0, 28))

        # Placar Agente, alinhado à direita
        agent_rect = pygame.Rect(WIDTH/2, 0, WIDTH/2, 100)
        pygame.draw.rect(screen, chip_enum[1], agent_rect)
        text_a1 = font.render("Agente Inteligente", True, "Black")
        screen.blit(text_a1, (agent_rect.right-text_a1.get_rect().width, agent_rect.top))

        text_a2 = font.render(f"Última Jogada: {tempo[1]:.2f} s", True, "Black")
        screen.blit(text_a2, (agent_rect.right-text_a2.get_rect().width, text_a1.get_rect().height+4))

        text_a3 = font.render(f"f(x): {aval}", True, "Black")
        screen.blit(text_a3, (agent_rect.right-text_a3.get_rect().width, 2*(text_a2.get_rect().height+4)))


        # Layout tabuleiro
        pygame.draw.rect(screen, "Dark Blue", pygame.Rect(0, 100 + CHIP_SIZE, WIDTH, HEIGHT-CHIP_SIZE))
        pygame.draw.rect(screen, "Black", pygame.Rect(0, 100, WIDTH, CHIP_SIZE))

        tabuleiro_m = tabuleiro.toMatrix()

        for i in range(len(tabuleiro_m)):
            for j in range(len(tabuleiro_m[i])):
                pygame.draw.circle(screen, chip_enum[tabuleiro_m[i][j]], (CHIP_SIZE*j + CHIP_SIZE/2, CHIP_SIZE + 100 + CHIP_SIZE*i + CHIP_SIZE/2), CHIP_SIZE/2)

        pygame.draw.circle(screen, chip_enum[curr_player], (CHIP_SIZE * column + CHIP_SIZE/2, CHIP_SIZE/2 + 100), CHIP_SIZE/2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and curr_player == PLAYER_HUMAN:
                if tabuleiro.canPlay(column):
                    if tabuleiro.solver(column):
                        game_ended = True
                        winner = curr_player
                        tabuleiro.add_chip(column)
                        tabuleiro.changePlayer()
                    else:
                        tabuleiro.add_chip(column)

                    tempo[curr_player] = (pygame.time.get_ticks() - start_time) / 1000
                    curr_player = PLAYER_AGENT
                    start_time = pygame.time.get_ticks()

        # Jogada do agente
        if not game_ended and curr_player == PLAYER_AGENT:
            start_time = pygame.time.get_ticks()

            if difficulty == 2:  #profissional com ids
                import time
                t0 = time.perf_counter()
                col, aval = agent.choose_move_time(tabuleiro, time_limit=3.0)
            elif difficulty == 1:  # intermediario com minimax ordenado
                col = agent.choose_move_alphabeta(tabuleiro, 5)
            else:  # iniciante com minimax simples
                col = agent.choose_move(tabuleiro, 3)
                aval = 0

            if tabuleiro.canPlay(col):
                if tabuleiro.solver(col):
                    game_ended = True
                    winner = PLAYER_AGENT

                tabuleiro.add_chip(col)

                tempo[PLAYER_AGENT] = (pygame.time.get_ticks() - start_time) / 1000
                curr_player = PLAYER_HUMAN
                start_time = pygame.time.get_ticks()
            
        if tabuleiro.draw():
            game_ended = True

        pygame.display.update()
        clock.tick(30)

    tabuleiro_m = tabuleiro.toMatrix()

    for i in range(len(tabuleiro_m)):
        for j in range(len(tabuleiro_m[i])):
            pygame.draw.circle(screen, chip_enum[tabuleiro_m[i][j]], (CHIP_SIZE*j + CHIP_SIZE/2, CHIP_SIZE + 100 + CHIP_SIZE*i + CHIP_SIZE/2), CHIP_SIZE/2)

    victor_rect = pygame.Rect(0, 0, WIDTH, 100)
    pygame.draw.rect(screen, "White", victor_rect)
    result_text = "Empate!" if tabuleiro.draw() else f"Vitória do {'Humano' if winner == PLAYER_HUMAN else 'Agente'}!"
    end_text = font.render(result_text, True, "Black")
    screen.blit(end_text, (victor_rect.centerx-end_text.get_rect().width/2, victor_rect.centery-end_text.get_rect().height/2))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()