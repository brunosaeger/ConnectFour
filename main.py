import pygame
from sys import exit

def add_chip(column):
    """
    Se for possível colocar uma peça nessa coluna, adiciona a peça e retorna True, senão, não faz nada e retorna False
    """
    if tabuleiro[0][column] != 2:
        return False
    
    for i in range(5, -1, -1):
        if tabuleiro[i][column] == 2:
            tabuleiro[i][column] = curr_player
            break
    
    return True

WIDTH = 700
HEIGHT = 800
CHIP_SIZE = 100

tabuleiro = [[2 for _ in range(7)] for _ in range(6)]

chip_enum = ["Red", "Yellow", "Blue"]

curr_player = 0
game_ended = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

start_time = 0
tempo = [0, 0]
aval = 0

while not game_ended:
    mouse_pos = pygame.mouse.get_pos()
    column = mouse_pos[0] // CHIP_SIZE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_chip(column):
                tempo[curr_player] = (pygame.time.get_ticks() - start_time) / 1000
                curr_player = (curr_player + 1) % 2
                start_time = pygame.time.get_ticks()

    pygame.draw.rect(screen, chip_enum[0], pygame.Rect(0, 0, WIDTH/2, 100))
    screen.blit(font.render("Agente Humano", True, "Black"), (0, 0))
    screen.blit(font.render(f"Última Jogada: {tempo[0]:.2f} s", True, "Black"), (0, 28))

    pygame.draw.rect(screen, chip_enum[1], pygame.Rect(WIDTH/2, 0, WIDTH/2, 100))
    screen.blit(font.render("Agente Inteligente", True, "Black"), (WIDTH/2, 0))
    screen.blit(font.render(f"Última Jogada: {tempo[1]:.2f} s", True, "Black"), (WIDTH/2, 28))
    screen.blit(font.render(f"f(x): {aval}", True, "Black"), (WIDTH/2, 56))

    pygame.draw.rect(screen, "Dark Blue", pygame.Rect(0, 100 + CHIP_SIZE, WIDTH, HEIGHT-CHIP_SIZE))
    pygame.draw.rect(screen, "Black", pygame.Rect(0, 100, WIDTH, CHIP_SIZE))

    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            pygame.draw.circle(screen, chip_enum[tabuleiro[i][j]], (CHIP_SIZE*j + CHIP_SIZE/2, CHIP_SIZE + 100 + CHIP_SIZE*i + CHIP_SIZE/2), CHIP_SIZE/2)

    pygame.draw.circle(screen, chip_enum[curr_player], (CHIP_SIZE * column + CHIP_SIZE/2, CHIP_SIZE/2 + 100), CHIP_SIZE/2)

    pygame.display.update()
    clock.tick(30)