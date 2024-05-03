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
  return render_template('index.html', board=board)

if __name__ == '__main__':
  app.run(debug=True)

@app.route('/check-word', methods=['POST'])
def check_word():
  word = request.json['word']
  board = session.get('board', [])
  response = boggle_game.check_valid_word(board, word)
  return jsonify({'result': response})