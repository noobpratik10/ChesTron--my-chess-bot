import pickle
import numpy as np
from keras.models import load_model
import chess

def load_model_and_mapping():
    """
    Load a saved model and move-to-int mapping.
    """
    #getting the path
    model_path = 'Engine/model_epoch_100.h5'
    mapping_path = 'Engine/move_to_int.pkl'

    # Load the trained model and mapping
    model = load_model(model_path)
    with open(mapping_path, 'rb') as f:
        move_to_int = pickle.load(f)

    # Create the inverse mapping (int to move)
    int_to_move = {v: k for k, v in move_to_int.items()}

    return model, move_to_int, int_to_move

def board_to_matrix(board: chess.Board):
    """
    Convert board to its matrix representation.
    """
    # 8x8 is a size of the chess board.
    # 12 = number of unique pieces.
    # 13th board for legal moves (WHERE we can move)
    matrix = np.zeros((13, 8, 8))
    piece_map = board.piece_map()

    # Populate first 12 8x8 boards (where pieces are)
    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        piece_type = piece.piece_type - 1
        piece_color = 0 if piece.color else 6
        matrix[piece_type + piece_color, row, col] = 1

    # Populate the legal moves board (13th 8x8 board)
    legal_moves = board.legal_moves
    for move in legal_moves:
        to_square = move.to_square
        row_to, col_to = divmod(to_square, 8)
        matrix[12, row_to, col_to] = 1

    return matrix


def get_best_move_cnn(board):
    """
    Given a chess board state, use the model to predict the best move.
    """
    #Load the model & mapping
    model, move_to_int, int_to_move = load_model_and_mapping()

    #Predict the best moves using the model
    board_state = board_to_matrix(board)
    model_input = np.expand_dims(board_state, axis=0)

    predictions = model.predict(model_input)[0]
    sorted_indices = np.argsort(predictions)[::-1]

    #return the best legal move
    legal_moves = list(board.legal_moves)
    legal_moves_uci = [move.uci() for move in legal_moves]
    for move_index in sorted_indices:
            move = int_to_move[move_index]  # Map the index to the corresponding move in UCI format
            if move in legal_moves_uci:
                return chess.Move.from_uci(move)  # Return the legal move as a chess.Move object

    # print('No legal moves found.')
    return legal_moves[0]
