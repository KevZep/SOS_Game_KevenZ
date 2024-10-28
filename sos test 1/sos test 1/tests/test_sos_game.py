import unittest
from src.game_logic import SimpleGame, GeneralGame, Board, GameMode

class TestSOSGame(unittest.TestCase):
    """Test cases for SOS game covering both Simple and General modes."""

    def test_choose_board_size(self):
        """Test choosing a valid board size."""
        board = Board()
        board.set_board_size(5)
        self.assertEqual(board.size, 5)

    def test_invalid_board_size(self):
        """Test choosing an invalid board size."""
        board = Board()
        with self.assertRaises(ValueError):
            board.set_board_size(11)

    def test_choose_game_mode(self):
        """Test choosing a game mode."""
        game_mode = GameMode()
        game_mode.set_game_mode("Simple")
        self.assertEqual(game_mode.mode, "Simple")
        
        game_mode.set_game_mode("General")
        self.assertEqual(game_mode.mode, "General")

    def test_start_new_game_simple(self):
        """Test starting a new game in Simple mode."""
        game = SimpleGame(board_size=3)
        game.start_new_game()
        self.assertFalse(game.is_game_over())
        self.assertEqual(game.board.size, 3)
        self.assertEqual(game.mode, "Simple")

    def test_start_new_game_general(self):
        """Test starting a new game in General mode."""
        game = GeneralGame(board_size=4)
        game.start_new_game()
        self.assertFalse(game.is_game_over())
        self.assertEqual(game.board.size, 4)
        self.assertEqual(game.mode, "General")

    def test_make_move_simple_game(self):
        """Test making a move in a Simple game."""
        game = SimpleGame(board_size=3)
        game.start_new_game()
        game.make_move(0, 0, 'S')
        self.assertEqual(game.board.get_cell(0, 0), 'S')

    def test_simple_game_over(self):
        """Test that a Simple game is over when 'SOS' is formed."""
        game = SimpleGame(board_size=3)
        game.start_new_game()
        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'S')  # Forms 'SOS'
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.check_winner(), "Player 1")

    def test_make_move_general_game(self):
        """Test making a move in a General game."""
        game = GeneralGame(board_size=3)
        game.start_new_game()
        game.make_move(0, 0, 'S')
        self.assertEqual(game.board.get_cell(0, 0), 'S')

    def test_general_game_over(self):
        """Test that a General game is over when the board is full."""
        game = GeneralGame(board_size=3)
        game.start_new_game()
        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'S')
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'S')
        game.make_move(1, 2, 'O')
        game.make_move(2, 0, 'S')
        game.make_move(2, 1, 'O')
        game.make_move(2, 2, 'S')  # Board is now full
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.check_winner(), "Player 1")  # Assuming Player 1 formed more 'SOS'

if __name__ == '__main__':
    unittest.main()
