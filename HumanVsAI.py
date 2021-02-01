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


def calculate_window(window, piece):
    score = 0
    opponent_piece = 1
    if piece == 1:
        opponent_piece = 2

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 80
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 16
    elif window.count(piece) == 1 and window.count(EMPTY) == 3:
        score += 3

    if window.count(opponent_piece) == 4:
        score -= 10000
    elif window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    elif window.count(opponent_piece) == 2 and window.count(EMPTY) == 2:
        score -= 16
    elif window.count(opponent_piece) == 1 and window.count(EMPTY) == 3:
        score -= 3

    return score


def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_location(board)) == 0


def minimax(board, depth, alpha, beta, maxPlayer):
    valid_location = get_valid_location(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return None, 100000000
            elif winning_move(board, 1):
                return None, -100000000
            else:
                return None, 0
        else:
            return None, score_position(board, 2)

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

def score_position(board, piece):

    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 1

    # for hori
    for r in range(ROW_COUNT):
        row_arr = [int(val) for val in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_arr[c:c+WINDOW_LENGTH]
            score += calculate_window(window, piece)

    #for verti
    for c in range(COLUMN_COUNT):
        col_arr = [int(val) for val in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_arr[r:r+WINDOW_LENGTH]
            score += calculate_window(window, piece)

    #for positive slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += calculate_window(window, piece)

    #negative slope
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += calculate_window(window,piece)

    return score


def get_valid_location(board):
    valid_locations = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations

def pick_best_move(board,piece):
    valid_locations = get_valid_location(board)
    print(valid_locations)
    best_score = -1000
    best_col = random.choice(valid_locations)
    print("best_col by rand: ",best_col)

    for column in valid_locations:
        row = get_next_open_row(board,column)
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)
        score = score_position(temp_board, piece)

        if score > best_score:
            print("best in if: ",score, ' ', column)
            best_score = score
            best_col = column

    return best_col


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

            # col = random.randint(0,COLUMN_COUNT-1)
            # col = pick_best_move(board, 2)
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            # print('***************',col,'*******************')
            if is_valid_location(board, col):
                # pygame.time.wait(600)
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
