import chess
import time

# PESTO's Evaluation Function
# middle-game and end-game values
mg_value = [82, 337, 365, 477, 1025, 0]  # PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
eg_value = [94, 281, 297, 512, 936, 0]

# evaluation tables
pawn_table = {
    "mg": [
        0, 0, 0, 0, 0, 0, 0, 0,
        98, 134, 61, 95, 68, 126, 34, -11,
        -6, 7, 26, 31, 65, 56, 25, -20,
        -14, 13, 6, 21, 23, 12, 17, -23,
        -27, -2, -5, 12, 17, 6, 10, -25,
        -26, -4, -4, -10, 3, 3, 33, -12,
        -35, -1, -20, -23, -15, 24, 38, -22,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    "eg": [
        0, 0, 0, 0, 0, 0, 0, 0,
        178, 173, 158, 134, 147, 132, 165, 187,
        94, 100, 85, 67, 56, 53, 82, 84,
        32, 24, 13, 5, -2, 4, 17, 17,
        13, 9, -3, -7, -7, -8, 3, -1,
        4, 7, -6, 1, 0, -5, -1, -8,
        13, 8, 8, 10, 13, 0, 2, -7,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
}

knight_table = {
    "mg": [
        -167, -89, -34, -49, 61, -97, -15, -107,
        -73, -41, 72, 36, 23, 62, 7, -17,
        -47, 60, 37, 65, 84, 129, 73, 44,
        -9, 17, 19, 53, 37, 69, 18, 22,
        -13, 4, 16, 13, 28, 19, 21, -8,
        -23, -9, 12, 10, 19, 17, 25, -16,
        -29, -53, -12, -3, -1, 18, -14, -19,
        -105, -21, -58, -33, -17, -28, -19, -23
    ],
    "eg": [
        -58, -38, -13, -28, -31, -27, -63, -99,
        -25, -8, -25, -2, -9, -25, -24, -52,
        -24, -20, 10, 9, -1, -9, -19, -41,
        -17, 3, 22, 22, 22, 11, 8, -18,
        -18, -6, 16, 25, 16, 17, 4, -18,
        -23, -3, -1, 15, 10, -3, -20, -22,
        -42, -20, -10, -5, -2, -20, -23, -44,
        -29, -51, -23, -15, -22, -18, -50, -64
    ]
}

bishop_table = {
    "mg": [
        -29, 4, -82, -37, -25, -42, 7, -8,
        -26, 16, -18, -13, 30, 59, 18, -47,
        -16, 37, 43, 40, 35, 50, 37, -2,
        -4, 5, 19, 50, 37, 37, 7, -2,
        -6, 13, 13, 26, 34, 12, 10, 4,
        0, 15, 15, 15, 14, 27, 18, 10,
        4, 15, 16, 0, 7, 21, 33, 1,
        -33, -3, -14, -21, -13, -12, -39, -21
    ],
    "eg": [
        -14, -21, -11, -8, -7, -9, -17, -24,
        -8, -4, 7, -12, -3, -13, -4, -14,
        2, -8, 0, -1, -2, 6, 0, 4,
        -3, 9, 12, 9, 14, 10, 3, 2,
        -6, 3, 13, 19, 7, 10, -3, -9,
        -12, -3, 8, 10, 13, 3, -7, -15,
        -14, -18, -7, -1, 4, -9, -15, -27,
        -23, -9, -23, -5, -9, -16, -5, -17
    ]
}

rook_table = {
    "mg": [
        32, 42, 32, 51, 63, 9, 31, 43,
        27, 32, 58, 62, 80, 67, 26, 44,
        -5, 19, 26, 36, 17, 45, 61, 16,
        -24, -11, 7, 26, 24, 35, -8, -20,
        -36, -26, -12, -1, 9, -7, 6, -23,
        -45, -25, -16, -17, 3, 0, -5, -33,
        -44, -16, -20, -9, -1, 11, -6, -71,
        -19, -13, 1, 17, 16, 7, -37, -26,
    ],
    "eg": [
        13, 10, 18, 15, 12, 12, 8, 5,
        11, 13, 13, 11, -3, 3, 8, 3,
        7, 7, 7, 5, 4, -3, -5, -3,
        4, 3, 13, 1, 2, 1, -1, 2,
        3, 5, 8, 4, -5, -6, -8, -11,
        -4, 0, -5, -1, -7, -12, -8, -16,
        -6, -6, 0, 2, -9, -9, -11, -3,
        -9, 2, 3, -1, -5, -13, 4, -20
    ]
}

queen_table = {
    "mg": [
        -28, 0, 29, 12, 59, 44, 43, 45,
        -24, -39, -5, 1, -16, 57, 28, 54,
        -13, -17, 7, 8, 29, 56, 47, 57,
        -27, -27, -16, -16, -1, 17, -2, 1,
        -9, -26, -9, -10, -2, -4, 3, -3,
        -14, 2, -11, -2, -5, 2, 14, 5,
        -35, -8, 11, 2, 8, 15, -3, 1,
        -1, -18, -9, 10, -15, -25, -31, -50
    ],
    "eg": [
        -9, 22, 22, 27, 27, 19, 10, 20,
        -17, 20, 32, 41, 58, 25, 30, 0,
        -20, 6, 9, 49, 47, 35, 19, 9,
        3, 22, 24, 45, 57, 40, 57, 36,
        -18, 28, 19, 47, 31, 34, 39, 23,
        -16, -27, 15, 6, 9, 17, 10, 5,
        -22, -23, -30, -16, -16, -23, -36, -32,
        -33, -28, -22, -43, -5, -32, -20, -41
    ]
}

king_table = {
    "mg": [
        -65, 23, 16, -15, -56, -34, 2, 13,
        29, -1, -20, -7, -8, -4, -38, -29,
        -9, 24, 2, -16, -20, 6, 22, -22,
        -17, -20, -12, -27, -30, -25, -14, -36,
        -49, -1, -27, -39, -46, -44, -33, -51,
        -14, -14, -22, -46, -44, -30, -15, -27,
        1, 7, -8, -64, -43, -16, 9, 8,
        -15, 36, 12, -54, 8, -28, 24, 14
    ],
    "eg": [
        -74, -35, -18, -18, -11, 15, 4, -17,
        -12, 17, 14, 17, 17, 38, 23, 11,
        10, 17, 23, 15, 20, 45, 44, 13,
        -8, 22, 24, 27, 26, 33, 26, 3,
        -18, -4, 21, 24, 27, 23, 9, -11,
        -19, -3, 11, 21, 23, 16, 7, -9,
        -27, -11, 4, 13, 14, 4, -5, -17,
        -53, -34, -21, -11, -28, -14, -24, -43
    ]
}

mg_pesto_table = [
    pawn_table["mg"],
    knight_table["mg"],
    bishop_table["mg"],
    rook_table["mg"],
    queen_table["mg"],
    king_table["mg"]
]
eg_pesto_table = [
    pawn_table["eg"],
    knight_table["eg"],
    bishop_table["eg"],
    rook_table["eg"],
    queen_table["eg"],
    king_table["eg"]
]

# Game phase increments
gamephase_inc = [0, 0, 1, 1, 1, 1, 2, 2, 4, 4, 0, 0]

# Evaluation tables
mg_table = [[0] * 64 for _ in range(12)]
eg_table = [[0] * 64 for _ in range(12)]


# Helper functions
def flip_square(square):
    """
    Flip the square vertically (for perspective inversion).
    """
    return square ^ 56

def init_tables():
    """
    Initialize the evaluation tables
    """
    for p in range(6):  # Iterate piece types
        for sq in range(64):  # Iterate board squares
            # White pieces
            mg_table[2 * p][sq] = mg_value[p] + mg_pesto_table[p][sq]
            eg_table[2 * p][sq] = eg_value[p] + eg_pesto_table[p][sq]
            # Black pieces (flip the board)
            mg_table[2 * p + 1][sq] = mg_value[p] + mg_pesto_table[p][flip_square(sq)]
            eg_table[2 * p + 1][sq] = eg_value[p] + eg_pesto_table[p][flip_square(sq)]


def pesto_evaluate(board: chess.Board):
    """
    Evaluate the board position
    """
    mg = [0, 0]  # Middle game scores for WHITE and BLACK
    eg = [0, 0]  # End game scores for WHITE and BLACK
    game_phase = 0
    side_to_move = 0  if(board.turn == chess.WHITE) else 1  # 0 WHITE 1 BLACK

    # Iterate over all squares
    for sq in range(64):
        # Get the piece at the square
        pc = board.piece_at(sq)
        if pc is not None:
            color = pc.color
            pc_index = 2 * (pc.piece_type - 1) + color  # Convert to the custom piece encoding
            mg[color] += mg_table[pc_index][sq]
            eg[color] += eg_table[pc_index][sq]
            game_phase += gamephase_inc[pc_index]

    # Tapered evaluation
    mg_score = mg[side_to_move] - mg[1 - side_to_move]  # mg[1 - side_to_move] is the other player's score
    eg_score = eg[side_to_move] - eg[1 - side_to_move]

    mg_phase = game_phase
    if mg_phase > 24:
        mg_phase = 24  # In case of early promotion

    eg_phase = 24 - mg_phase

    # Return the final evaluation
    return (mg_score * mg_phase + eg_score * eg_phase) // 24


def alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    Alpha-Beta pruning with Berliner's evaluation system.
    :param board: object
    :param depth: depth of search tree
    :param alpha:
    :param beta:
    :param maximizing_player: turn
    :return: value
    """
    if depth == 0 or board.is_game_over():
        return pesto_evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval


def get_best_move_ab(board, max_depth=5, time_limit=5):
    """
    Iterative deepening with alpha-beta pruning and time control.
    :param board: chess.Board object
    :param max_depth: maximum depth for search
    :param time_limit: time limit in seconds
    :return: best move
    """

    init_tables()
    start_time = time.time()
    best_move = None

    for depth in range(1, max_depth + 1):
        if time.time() - start_time > time_limit:
            # print("Time limit reached, returning best move found so far.")
            break

        current_best_move = None
        best_value = float('-inf') if board.turn == chess.WHITE else float('inf')

        for move in board.legal_moves:
            board.push(move)
            move_value = alpha_beta(board, depth - 1, float('-inf'), float('inf'), board.turn)
            board.pop()

            if board.turn == chess.WHITE:
                if move_value > best_value:
                    best_value = move_value
                    current_best_move = move
            else:
                if move_value < best_value:
                    best_value = move_value
                    current_best_move = move


        best_move = current_best_move
        # Debug output for depth
        # print(f"Depth {depth}: Best move so far: {best_move}, Value: {best_value}")

    return best_move
