import random
import numpy as np
import pygame
import sys
import math
import Gui as gui


BLUE = (190, 229, 211)
BLACK = (17, 29, 100)
RED = (255, 87, 127)
YELLOW = (200, 200, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
sizeOfSquare = 75
RADIUS = int(sizeOfSquare / 2 - 5)
PLAYER = 0
AI = 1


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def play(screen, width, height, board):
    fonts = pygame.font.SysFont("monospace", 60)
    game_over = False
    turn = random.randint(PLAYER,AI)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, sizeOfSquare))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(sizeOfSquare / 2)), RADIUS)
                # else:
                #     pygame.draw.circle(screen, YELLOW, (posx, int(sizeOfSquare / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, sizeOfSquare))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / sizeOfSquare))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = fonts.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (5, 10))
                            game_over = True
                            # pygame.time.wait(3500)
                                
                        turn += 1
                        turn = turn % 2
                        print_board(board)
                        gui.draw_board(board, screen, height)

        if turn == AI and not game_over:

            col = random.randint(0,COLUMN_COUNT-1)

            if is_valid_location(board, col):
                pygame.time.wait(600)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = fonts.render("AI wins!", 1, YELLOW)
                    screen.blit(label, (5, 10))
                    game_over = True

                print_board(board)
                gui.draw_board(board, screen, height)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3500)


def main():
    board = gui.create_board()
    print_board(board)

    pygame.init()

    width = COLUMN_COUNT * sizeOfSquare
    height = (ROW_COUNT + 1) * sizeOfSquare

    size = (width, height)

    screen = pygame.display.set_mode(size)
    gui.draw_board(board, screen, height)
    pygame.display.update()

    play(screen, width, height, board)


if __name__ == '__main__':
    main()
