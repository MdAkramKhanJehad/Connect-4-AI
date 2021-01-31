import numpy as np
import pygame


BLUE = (190, 229, 211)
BLACK = (17, 29, 100)
RED = (255, 87, 127)
YELLOW = (200, 200, 0)


ROW_COUNT = 6
COLUMN_COUNT = 7
sizeOfSquare = 75
RADIUS = int(sizeOfSquare / 2 - 5)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def draw_board(board, screen, height):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * sizeOfSquare, r * sizeOfSquare + sizeOfSquare, sizeOfSquare, sizeOfSquare))
            pygame.draw.circle(screen, BLACK, (int(c * sizeOfSquare + sizeOfSquare / 2), int(r * sizeOfSquare + sizeOfSquare + sizeOfSquare / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * sizeOfSquare + sizeOfSquare / 2), height - int(r * sizeOfSquare + sizeOfSquare / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * sizeOfSquare + sizeOfSquare / 2), height - int(r * sizeOfSquare + sizeOfSquare / 2)), RADIUS)
    pygame.display.update()

