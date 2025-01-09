# ChesTron - My Chess Bot

## Overview
**ChesTron** is a user-friendly web application that lets you play chess against AI-powered bots. ChesTron provides an engaging experience with two powerful chess engines:  
- **PRUNER**: Built on the Minimax algorithm with Alpha-Beta pruning, enhanced using the renowned PESTO evaluation tables for dynamic game analysis.  
- **CNINGA**: A deep convolutional neural network (CNN) trained on 100,000+ high-level games from Lichess (2300+ rating), delivering advanced gameplay patterns and insights.  

## Demo
- The web application has been deployed on Render for reliable hosting. Check it out now: [ChesTron Web App](https://chestron-my-chess-bot.onrender.com).
  
## Features
- Interactive chessboard for human-vs-AI gameplay.
- Seamless user interface optimized for desktop.
- Intelligent move suggestions and analysis based on game phase.
- Switch between PRUNER (logic-driven) and CNINGA (data-driven) chess engines.  

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Flask (Python), enabling API-driven interactions with the chess engines.  
- **AI Algorithms**:  
  - Minimax with Alpha-Beta pruning for PRUNER.  
  - TensorFlow/Keras for training and deploying CNINGA.  
- **Evaluation**: PESTO evaluation tables for optimized middle-game and end-game assessments.  

## Installation  
Follow these steps to get ChesTron running locally:  
1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/ChesTron.git
   cd ChesTron
   ```  
2. Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Run the Flask application:  
   ```bash
   python app.py
   ```  
