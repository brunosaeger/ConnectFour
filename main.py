import pygame
import numpy as np
from sys import exit
from board import Board

if __name__ == "__main__":
    WIDTH = 700
    HEIGHT = 800
    CHIP_SIZE = 100

    tabuleiro = Board()

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

        for i in range(len(tabuleiro.board)):
            for j in range(len(tabuleiro.board[i])):
                pygame.draw.circle(screen, chip_enum[tabuleiro.board[i][j]], (CHIP_SIZE*j + CHIP_SIZE/2, CHIP_SIZE + 100 + CHIP_SIZE*i + CHIP_SIZE/2), CHIP_SIZE/2)

        pygame.draw.circle(screen, chip_enum[curr_player], (CHIP_SIZE * column + CHIP_SIZE/2, CHIP_SIZE/2 + 100), CHIP_SIZE/2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                success, index = tabuleiro.add_chip(column, curr_player)

                if success:
                    if tabuleiro.solver(curr_player, index, column):
                        game_ended = True
                        winner = curr_player
                    
                    tempo[curr_player] = (pygame.time.get_ticks() - start_time) / 1000
                    curr_player = (curr_player + 1) % 2
                    start_time = pygame.time.get_ticks()

        pygame.display.update()
        clock.tick(30)