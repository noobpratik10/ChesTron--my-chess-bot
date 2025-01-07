# Web based GUI for my chess engine

#packages
from flask import Flask
from flask import render_template
from flask import request
import chess
from Engine.alphabeta import get_best_move_ab
from Engine.cnn_model import get_best_move_cnn

#create web app instance
app = Flask(__name__)

#root(index) route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET'])
def play():
    opponent = request.args.get('opponent', 'Option1')  # Default to Option1 (MinMax)
    return render_template('play.html', opponent=opponent)

#moke_move route
@app.route('/make_move',methods=['POST'])
def make_move():
    #extract FEN string from HTTP POST request body
    fen=request.form.get('fen')
    opponent=request.form.get('opponent')

    #initialize python chess board
    board = chess.Board(fen)

    #search for best move
    if opponent == 'Option1':
        move = get_best_move_ab(board)      #MinMax Algo
    else:
        move = get_best_move_cnn(board)     #CNN Model

    #update internal python board state
    board.push(move)

    #extract fen from current board state
    fen=board.fen()

    return {'fen':fen, 'best_move':str(move)}

#main driver
if __name__ == '__main__':
    #start HTTP server
    app.run(debug=True,threaded=True)