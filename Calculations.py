from HumanVsAI import WINDOW_LENGTH


ROW_COUNT = 6
COLUMN_COUNT = 7


def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:,3])]
    center_count = center_array.count(piece)
    score += center_count * 1

    for r in range(ROW_COUNT):
        row_arr = [int(val) for val in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_arr[c:c+WINDOW_LENGTH]
            score += calculate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_arr = [int(val) for val in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_arr[r:r+WINDOW_LENGTH]
            score += calculate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += calculate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += calculate_window(window,piece)

    return score


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def calculate_window(window, piece):
    score = 0
    opponent_piece = 1
    if piece == 1:
        opponent_piece = 2

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 80
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 16
    elif window.count(piece) == 1 and window.count(0) == 3:
        score += 3

    if window.count(opponent_piece) == 4:
        score -= 10000
    elif window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 80
    elif window.count(opponent_piece) == 2 and window.count(0) == 2:
        score -= 16
    elif window.count(opponent_piece) == 1 and window.count(0) == 3:
        score -= 3

    return score


