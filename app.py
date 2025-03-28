# Web based GUI for my chess engine

#packages
from flask_pymongo import PyMongo
from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import chess
from Engine.alphabeta import get_best_move_ab
from Engine.cnn_model import get_best_move_cnn
import os

import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#create web app instance
app = Flask(__name__)

#add db
app.config["MONGO_URI"] = "mongodb://localhost:27017/Chestron"
mongo = PyMongo(app)

# Set secret_key from environment variable
app.secret_key = os.getenv('FLASK_SECRET_KEY')

#Set secret key of Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

#root(index) route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play', methods=['GET'])
def play():
    opponent = request.args.get('opponent', 'Option1')  # Default to Option1 (MinMax)
    pgn = request.args.get('pgn', '')
    status = request.args.get('status', '')
    fen = request.args.get('fen', '')

    # Get the username from the session
    username = session.get("user")

    # Default values if no user is logged in
    user_data = None

    if username:
        # Query the database for the logged-in user's information
        users = mongo.db.Users
        user_data = users.find_one({"username": username})

    return render_template('play.html', opponent=opponent,pgn=pgn, status=status, fen=fen, user=user_data)


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

@app.route('/home')
def home():
    return render_template('home.html')


# Sign Up Route
@app.route("/signup", methods=["POST"])
def signup():
    users = mongo.db.Users  # Users collection
    name = request.form.get("name")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    rating = request.form.get("rating")

    # Check if username already exists
    if users.find_one({"username": username}):
        return jsonify({"success": False, "message": "Username already exists!"})

    # Handle file upload (image)
    profile_pic = request.files.get("profile_pic")
    image_url = None

    if profile_pic:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(profile_pic)
        image_url = upload_result["secure_url"]  # Cloudinary URL of the uploaded image

    # Store user in the database
    hashed_password = generate_password_hash(password)
    users.insert_one({
        "name": name,
        "email": email,
        "username": username,
        "password": hashed_password,
        "rating": rating,
        "profile_pic_url": image_url  # Store the Cloudinary URL
    })

    return jsonify({"success": True})



# Login Route
@app.route("/login", methods=["POST"])
def login():
    users = mongo.db.Users
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        session["user"] = username  # Store session
        return jsonify({"success": True})

    return jsonify({"success": False})


#Save the Game
@app.route('/save_game', methods=['POST'])
def save_game():
    # Ensure the request is JSON
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'}), 415

    data = request.get_json()  # Use get_json() instead of request.json

    username = session.get('user')
    status = data.get('status')
    pgn = data.get('pgn')
    timestamp = data.get('timestamp')
    save_type = data.get('type')  # 'history' for completed games, 'saved' for unfinished games
    opponent = data.get('opponent')
    fen = data.get('fen')

    if not status or not pgn or not timestamp or not save_type or not opponent or not fen:
        return jsonify({'message': 'Invalid data'}), 400

    # Prepare game data
    game_data = {
        'status': status,
        'pgn': pgn,
        'timestamp': timestamp,
        'opponent': opponent,
        'fen': fen
    }

    # Save game in appropriate collection based on type
    if save_type == 'history':
        mongo.db.Users.update_one(
            {'username': username},
            {'$push': {'history': game_data}}
        )
    elif save_type == 'saved':
        mongo.db.Users.update_one(
            {'username': username},
            {'$push': {'saved_games': game_data}}
        )
    else:
        return jsonify({'message': 'Invalid game type'}), 400

    return jsonify({'message': 'Game saved successfully'}), 200

#load game
@app.route('/load_game')
def load_game():
    # Get current user from session
    username = session.get('user')

    if username:
        # Fetch user details from the database
        user = mongo.db.Users.find_one({'username': username})

        if user:
            # Fetch saved games for the user
            saved_games = sorted(user.get('saved_games', []), key=lambda x: x['timestamp'], reverse=True)
        else:
            saved_games = []
    else:
        user = None
        saved_games = []

    # Pass user details and saved games to the template
    return render_template('load_game.html', user=user, saved_games=saved_games)

# delete game
@app.route('/delete_game', methods=['POST'])
def delete_game():
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'}), 415

    data = request.get_json()
    username = session.get('user')  # Assuming the user is logged in
    pgn = data.get('pgn')
    status = data.get('status')
    timestamp = data.get('timestamp')

    if not pgn or not status or not timestamp:
        return jsonify({'message': 'Invalid data'}), 400

    # Remove the saved game/ history from the database
    mongo.db.Users.update_one(
        {'username': username},
        {'$pull': {'saved_games': {'pgn': pgn, 'status': status, 'timestamp': timestamp}}}
    )

    mongo.db.Users.update_one(
        {'username': username},
        {'$pull': {'history': {'pgn': pgn, 'status': status, 'timestamp': timestamp}}}
    )

    return jsonify({'message': 'Game deleted successfully'}), 200

@app.route('/history')
def history():
    # Get current user from session
    username = session.get('user')

    if username:
        # Fetch user details from the database
        user = mongo.db.Users.find_one({'username': username})

        if user:
            # Fetch history for the user
            history = sorted(user.get('history', []), key=lambda x: x['timestamp'], reverse=True)
        else:
            history = []
    else:
        user = None
        history = []

    # Pass user details and saved games to the template
    return render_template('history.html', user=user, history=history)

#main driver
if __name__ == '__main__':
    #start HTTP server
    app.run(debug=True,threaded=True)