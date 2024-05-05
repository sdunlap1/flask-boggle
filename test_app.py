from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTestes(TestCase):
  def setUp(self):
      """Set up the test client before each test.
         This method initializes the Flask test client 
         and configures the app for testing. Testing 
         configuration can include disabling CSRF protections 
         or other production security measures."""
      self.client = app.test_client()
      app.config['TESTING'] = True

  def test_homepage(self):
      """Test the homepage to ensure it loads properly and 
         the game board is initialized correctly. This method 
         checks if the homepage responds with a 200 status 
         code indicating success, and it verifies that a game 
         board has been created and stored in the session."""
      with self.client as client:
         response = client.get('/')
         self.assertEqual(response.status_code, 200)
         self.assertIn('board', session)
         self.assertEqual(len(session['board']), 5) # Assumes board is alwasy 5 X 5

  def test_check_word(self):
      """Test the check-word route to ensure it correctly validates 
         words against the Boggle board. This test manually sets a 
         board in the session and then checks a word to see if it is 
         recognized correctly by the route."""
      with self.client as client:
         with client.session_transaction() as sess:
            sess['board'] = [['S', 'T', 'E', 'V', 'E'],
                             ['S', 'T', 'E', 'V', 'E'],
                             ['S', 'T', 'E', 'V', 'E'],
                             ['S', 'T', 'E', 'V', 'E'],
                             ['S', 'T', 'E', 'V', 'E']]
            sess['submitted_words'] = []
      
      response = client.post('/check-word', json={'word': 'STEVE'})
      self.assertEqual(response.status_code, 200)
      self.assertIn('result', response.json)
      self.assertEqual(response.json['result'], 'ok')

  def test_post_score(self):
     """Test the post-score route to ensure it correctly receives scores 
        and updates session data. This method tests whether the route can 
        handle score submissions and properly updates the high score in the session."""
     with self.client as client:
        response = client.post('/post-score', json={'score': 10})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json)
        self.assertTrue(response.json['success'])
        self.assertEqual(session['high_score'], 10)

