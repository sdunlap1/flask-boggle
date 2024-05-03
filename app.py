from flask import Flask, request, session, render_template, redirect, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development'

boggle_game = Boggle()

@app.route('/')
def homepage():
  """Display the board"""
  board = boggle_game.make_board()
  session['board'] = board
  session['total_score'] = 0
  return render_template('index.html', board=board, score=session['total_score'])

if __name__ == '__main__':
  app.run(debug=True)

@app.route('/check-word', methods=['POST'])
def check_word():
    ("Received JSON:", request.json)
    
    # Extract word from JSON
    word = request.json['word']
    ("Processed word:", word)
    
    # Retrieve current game board from session: Default is empty
    board = session.get('board', [])
    ("Current board:", board)
    
    # Convert the list of submitted words stored in the session back to a set for manipulation
    # If 'submitted_words' is not in the session, initialize it as an empty set
    submitted_words = set(session.get('submitted_words', [])) 
    ("Submitted words before addition:", submitted_words)
    
    # Chekci if the word has already been submitted in the current game session
    if word in submitted_words:
        ("Word already submitted:", word)
        
        # If the word was already submitted don't count is again
        return jsonify({'result': 'already-submitted', 'score': session['total_score']})
    
    # Checks if word is vaild
    response = boggle_game.check_valid_word(board, word)
    ("Validation response:", response)
    
    # If the word is valid...
    if response == 'ok':
        # Calculate the score based on the length of the word
        score = len(word)
        # Add to the total score
        session['total_score'] = session.get('total_score', 0) + score
        # Add word to submitted words
        submitted_words.add(word)  
        ("Updated submitted words:", submitted_words)
        
        # Convert the set of submitted words back to a list to store in the session
        # This is necessary because sets are not JSON serializable and cannot be directly stored in sessions
        session['submitted_words'] = list(submitted_words)  
    ("Final response to send:", {'result': response, 'score': session['total_score']})
    
    # Return results and current score
    return jsonify({'result': response, 'score': session['total_score']})
