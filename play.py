from Engine.alphabeta import get_best_move_ab
from Engine.cnn_model import get_best_move_cnn
import chess

def play_game():
    """
    Function to play a game
    """
    print('Welcome to ChesTron!!')
    print('Choose your opponent:')
    print('1. PRUNER')
    print('2. CNINGA')

    while True:
        choice = int(input('Enter your choice: '))
        if choice == 1 or choice == 2:
            break
        else:
            print('Invalid choice, please try again.')


    print('You are White, Enter your moves in UCI format.')

    board = chess.Board()
    while not board.is_game_over():
        print(board)

        if board.turn == chess.WHITE:
            # player turn
            move = None
            while move not in board.legal_moves:
                user_input = input("Your move: ")
                try:
                    move = chess.Move.from_uci(user_input)
                    if move not in board.legal_moves:
                        print("Illegal move. Try again.")
                except ValueError:
                    print("Invalid input. Enter moves in UCI format (e.g., e2e4).")
            board.push(move)
            print(f'You played {move}.')
        else:
            # engine turn
            if choice == 1:
                move = get_best_move_ab(board)
            else:
                move = get_best_move_cnn(board)  # depth 5
            board.push(move)
            print(f'Engine played {move}.')

    print('Game over!!')
    print('Result: ', board.result())


# play the game
if __name__ == '__main__':
    play_game()
