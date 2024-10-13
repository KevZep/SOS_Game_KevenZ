# tests/test_sos_game.py
import unittest
from src.game_logic import GameLogic
from src.ui import SOSGameUI
import tkinter as tk

class TestGameLogic(unittest.TestCase):

    # AC 1.1: Test board size creation
    def test_board_size_creation(self):
        game = GameLogic(5)
        self.assertEqual(len(game.grid), 5)
        self.assertEqual(len(game.grid[0]), 5)

    # AC 1.2: Test invalid board size
    def test_invalid_board_size(self):
        with self.assertRaises(ValueError) as context:
            game = GameLogic(2)  # Invalid size, should raise an error
        self.assertEqual(str(context.exception), "Size must be between 3 and 10.")

    # AC 4.1: Test making a move
    def test_make_move(self):
        game = GameLogic(3)
        success = game.place_letter(0, 0, 'S')
        self.assertTrue(success)
        self.assertEqual(game.grid[0][0], 'S')

    # AC 4.2: Test switching turns
    def test_turn_switching(self):
        game = GameLogic(3)
        game.place_letter(0, 0, 'S')
        self.assertEqual(game.current_turn, 'Red')  # Turn should switch to Red after Blue's move

    # AC 5.1: Test SOS detection
    def test_sos_detection(self):
        game = GameLogic(3)
        game.place_letter(0, 0, 'S')
        game.place_letter(0, 1, 'O')
        game.place_letter(0, 2, 'S')
        self.assertTrue(game.check_sos(0, 2))  # Should detect SOS horizontally

    # AC 6.1: Test board full detection
    def test_board_full_detection(self):
        game = GameLogic(3)
        for row in range(3):
            for col in range(3):
                game.place_letter(row, col, 'S')
        self.assertTrue(game.is_full())

class TestSOSGameUI(unittest.TestCase):

    # AC 2.1: Test game mode display
    def test_game_mode_display(self):
        root = tk.Tk()
        app = SOSGameUI(root, game_logic=GameLogic(3))
        self.assertIsNotNone(app)  # Ensures the UI initializes
        # This test is simplified; GUI tests usually require mocks or manual inspection

if __name__ == "__main__":
    unittest.main()
