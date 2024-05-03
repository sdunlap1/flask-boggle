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
  word = request.json['word']
  board = session.get('board', [])
  response = boggle_game.check_valid_word(board, word)

  if response == 'ok':
    score = len(word)
    session['total_score'] = session.get('total_score', 0) + score
  return jsonify({'result': response, 'score': session.get('total_score', 0)})