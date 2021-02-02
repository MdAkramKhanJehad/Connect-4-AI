import random
import numpy as np
import pygame
import sys
import math
import Gui as gui
import Calculations as calc


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
WINDOW_LENGTH = 4
EMPTY = 0

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


def is_terminal_node(board):
    return calc.winning_move(board, 1) or calc.winning_move(board, 2) or len(get_valid_location(board)) == 0


def minimax(board, depth, alpha, beta, maxPlayer):
    valid_location = get_valid_location(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if calc.winning_move(board, 2):
                return None, 100000000
            elif calc.winning_move(board, 1):
                return None, -100000000
            else:
                return None, 0
        else:
            return None, calc.score_position(board, 2)

    if maxPlayer:
        value = -math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col,2)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row =  get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board,depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break

        return column, value



def get_valid_location(board):
    valid_locations = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations


def play(screen, width, height, board):
    fonts = pygame.font.SysFont("monospace", 60)
    game_over = False
    turn = random.randint(PLAYER,AI)

    while not game_over:
        if len(get_valid_location(board)) == 0:
            label = fonts.render("DRAW!!!", 1, YELLOW)
            screen.blit(label, (5, 10))
            gui.draw_board(board, screen, height)
            pygame.time.wait(3500)
            break


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, sizeOfSquare))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(sizeOfSquare / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, sizeOfSquare))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / sizeOfSquare))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if calc.winning_move(board, 1):
                            label = fonts.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (5, 10))
                            game_over = True
                            # pygame.time.wait(3500)
                                
                        turn += 1
                        turn = turn % 2
                        print_board(board)
                        gui.draw_board(board, screen, height)

        if turn == AI and not game_over:

            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if calc.winning_move(board, 2):
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
