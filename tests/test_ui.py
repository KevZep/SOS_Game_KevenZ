import unittest
from tkinter import Tk
from src.ui import SOSGameUI
from src.game_logic import GameLogic

class TestSOSGameUI(unittest.TestCase):
    def setUp(self):
        # Set up the root Tkinter window and game logic
        self.root = Tk()
        self.game_logic = GameLogic(size=3, mode="Simple")
        self.app = SOSGameUI(self.root, self.game_logic)

    def test_valid_board_size_initialization(self):
        # Test that the board initializes with the correct size
        self.app.size_entry.insert(0, '3')
        self.app.start_game()
        self.assertEqual(len(self.app.buttons), 3, "Board should be initialized with size 3x3")

    def test_invalid_board_size_handling(self):
        # Test that an invalid size triggers an error
        self.app.size_entry.insert(0, '11')  # Invalid size
        with self.assertRaises(ValueError):
            self.app.start_game()

    def test_display_turn_switch(self):
        # Check if turn label updates correctly after a move
        initial_turn = self.app.game_logic.current_turn
        self.app.on_grid_click(0, 0)  # Simulate a click on the grid
        new_turn = self.app.game_logic.current_turn
        self.assertNotEqual(initial_turn, new_turn, "Turn should switch after each move")
    
    def test_score_display_update(self):
        # Simulate SOS to update score and check if UI displays the change
        self.game_logic.board = [['S', 'O', ''], ['', '', ''], ['', '', '']]
        self.game_logic.current_turn = 'Blue'
        self.game_logic.place_letter(0, 2, 'S')
        self.app.update_scoreboard()
        
        self.assertIn("Blue: 1", self.app.scoreboard.cget("text"), "Scoreboard should update to reflect SOS")

    def tearDown(self):
        # Destroy the root window after each test
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
