"""Utilities related to Boggle game."""

from random import choice
import string


class Boggle():

    def __init__(self):

        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""
        try:
            with open(dict_path, 'r') as dict_file:
                words = {w.strip().upper() for w in dict_file}
        except FileNotFoundError:
            print(f"Dictionary file not found: {dict_path}")
            words = set()
        return words

    def make_board(self):
        """Make and return a random boggle board."""

        board = []

        for y in range(5):
            row = [choice(string.ascii_uppercase) for i in range(5)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""
        word = word.upper()
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())
        print(f"Checking word: {word}, Exists: {word_exists}, Valid on Board: {valid_word}")
        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result

    def find_from(self, board, word, y, x, seen):
         """Can we find a word on board, starting at x, y?

         This method is called recursively to find smaller and smaller words
         until all tries are exhausted or until success.
         """

         # Ensure coordinates are within the board bounds and word is not empty
         if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board) or not word:
            return False  # Prevents accessing out of bounds indices and handling empty words

         # Base case: this isn't the letter we're looking for.
         if board[y][x] != word[0]:
            return False

         # Base case: we've used this letter before in this current path
         if (y, x) in seen:
            return False

         # Base case: we are down to the last letter --- so we win!
         if len(word) == 1:
            return True

         # Otherwise, this letter is good, so note that we've seen it,
         # and try all of its neighbors for the first letter of the
         # rest of the word
         # We create a new set for seen to include the current cell
         new_seen = seen | {(y, x)}  # Includes the current cell without modifying the original seen set

         # Define directions for movement including diagonals
         directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),   # Up, Down, Left, Right
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
         ]

         # Recursively check all adjacent cells using the defined directions
         for dy, dx in directions:
            if self.find_from(board, word[1:], y + dy, x + dx, new_seen):
                return True  # If any direction confirms the word can be formed, return True

         # Couldn't find the next letter, so this path is dead
         return False


    def find(self, board, word):
        """Can word be found in board?"""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, 5):
            for x in range(0, 5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.

        return False
