import unittest
from src.game_logic import GameLogic

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game_logic_simple = GameLogic(size=3, mode="Simple")
        self.game_logic_general = GameLogic(size=3, mode="General")

    def test_ai_move_form_sos(self):
        # Arrange
        self.game_logic_simple.board = [['S', 'O', ''], ['', '', ''], ['', '', '']]
        self.game_logic_simple.current_turn = 'Red'
        
        # Act
        row, col, letter = self.game_logic_simple.ai_move()
        self.game_logic_simple.place_letter(row, col, letter)
        
        # Assert
        self.assertEqual(self.game_logic_simple.board[0][2], 'S', "AI should complete SOS")

    def test_general_mode_scoring(self):
        # Arrange
        self.game_logic_general.board = [['S', 'O', 'S'], ['', '', ''], ['', '', '']]
        self.game_logic_general.current_turn = 'Blue'
        
        # Act
        winner, sos_list = self.game_logic_general.place_letter(0, 2, 'S')
        
        # Assert
        self.assertEqual(self.game_logic_general.scores['Blue'], 1, "Score should update in General mode")

    def test_full_board_draw(self):
        # Fill the board without any SOS formed
        self.game_logic_general.board = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['S', 'O', 'S']
        ]
        
        # Assert that the game recognizes a draw
        self.assertTrue(self.game_logic_general.is_full(), "Board should be full")
        self.assertEqual(self.game_logic_general.check_winner_by_score(), 'Draw', "Game should end in a draw")

if __name__ == "__main__":
    unittest.main()

