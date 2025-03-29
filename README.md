### ChesTron -- My Chess Bot

#### Project Overview
ChesTron is a user-friendly web application that lets you play chess against AI-powered bots. It features two main AI bots:
- **PRUNER**: Built on Minimax with Alpha-Beta pruning using PESTO's evaluation.
- **CNINGA**: A Convolutional Neural Network (CNN) trained on 100,000+ Lichess games (2300+ ratings).

#### Features
- Play chess against advanced AI bots.
- PRUNER uses Minimax with Alpha-Beta pruning for efficient decision-making.
- CNINGA leverages deep learning techniques for competitive gameplay.

#### Deployment
Check out the app deployed on Render: [ChesTron - my chess bots](https://chestron-my-chess-bot.onrender.com)

#### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/noobpratik10/ChesTron--my-chess-bot.git
    ```
2. **Navigate to the project directory**:
    ```sh
    cd ChesTron--my-chess-bot
    ```
3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

#### Usage

1. **Run the Flask application**:
    ```sh
    python app.py
    ```
2. **Open your browser and navigate to**:
    ```sh
    http://localhost:5000
    ```

#### Demonstration
Here are some images demonstrating the working of the app:

![Game Start](images/game_start.png)
*Game Start Screen*

![In-Game](images/in_game.png)
*Playing against AI*

![Game End](images/game_end.png)
*Game Over Screen*
