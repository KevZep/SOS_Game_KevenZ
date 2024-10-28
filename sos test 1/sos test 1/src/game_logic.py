import random  # Import random module for selecting a starting player

class GameLogic:
    def __init__(self, size, mode='Simple', ui=None):
        # Initialize game parameters
        self.size = size  # Size of the game board
        self.mode = mode  # Game mode (Simple or General)
        self.board = [['' for _ in range(size)] for _ in range(size)]  # Create the game board
        self.current_turn = random.choice(['Blue', 'Red'])  # Randomly choose starting player
        self.scores = {'Blue': 0, 'Red': 0}  # Initialize scores
        self.moves = []  # To record moves for replay functionality
        self.ui = ui  # Reference to the UI for color changes

    def place_letter(self, row, col, letter):
        """Place a letter on the board and check for SOS formations."""
        if self.board[row][col] == '':
            self.board[row][col] = letter  # Place letter on the board
            self.moves.append((row, col, letter, self.current_turn))  # Record the move

            sos_list = self.check_for_sos(row, col, letter)  # Check for SOS formations

            if sos_list:  # If any SOS was formed
                self.scores[self.current_turn] += len(sos_list)  # Score points for unique SOS formations

                if self.ui:  # Check if UI is set
                    self.ui.color_squares(sos_list)  # Call to color squares for SOS

                # Check if the game should end in Simple mode
                if self.mode == 'Simple':
                    winner = self.current_turn  # Declare the current player as the winner
                    self.reset_game()  # Reset game for a new round
                    return winner, sos_list  # Return the winner and the SOS list

            # Switch turn after the current player has played
            self.current_turn = 'Red' if self.current_turn == 'Blue' else 'Blue'

            # Check for a winner in General mode if the board is full
            if self.is_full():
                winner = self.check_winner_by_score()  # Determine winner based on scores
                if winner:
                    return winner, None  # Return winner if found
                return 'Draw', None  # Return draw if no winner

            return None, None  # Continue game if no winner or draw

        return None, None  # Invalid move if the cell is already occupied

    def check_for_sos(self, row, col, letter):
        """Check for SOS formations based on the game mode."""
        if self.mode == 'Simple':
            return self.check_simple_sos(row, col, letter)  # Check for SOS in Simple mode
        elif self.mode == 'General':
            return self.check_general_sos(row, col, letter)  # Check for SOS in General mode
        return None  # No SOS found

    def check_simple_sos(self, row, col, letter):
        """Check for SOS in Simple mode (one SOS ends the game)."""
        sos_found, coordinates = self.is_sos(row, col)  # Check for SOS formation
        if sos_found:
            return [coordinates]  # Return SOS coordinates as a list for consistency
        return None  # No SOS found

    def check_general_sos(self, row, col, letter):
        """Check for SOS formations in General mode."""
        sos_list = []  # To track unique SOS formations
        checked_positions = set()  # Set to track unique SOS coordinates

        # Check all directions for SOS
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            sos_found, coordinates = self.is_sos_in_direction(row, col, dr, dc)  # Check for SOS in each direction
            if sos_found:
                # Convert coordinates to a frozenset for uniqueness
                coord_set = frozenset(coordinates)
                if coord_set not in checked_positions:
                    sos_list.append(coordinates)  # Collect unique SOS formations
                    checked_positions.add(coord_set)  # Mark as counted

        return sos_list if sos_list else None  # Return unique SOS list or None

    def is_sos(self, row, col):
        """Check if there's an SOS formation around the given position."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            sos_found, coordinates = self.is_sos_in_direction(row, col, dr, dc)  # Check in each direction
            if sos_found:
                return True, coordinates  # Return if SOS found
        return False, None  # No SOS found

    def is_sos_in_direction(self, row, col, dr, dc):
        """Check for SOS in a specific direction."""
        coordinates = []
    
        try:
            # Check for the 'O' letter
            if self.board[row][col] == 'O':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row - dr < self.size and 0 <= col - dc < self.size):
                    # Check for SOS formation with 'S' letters on both sides
                    if (self.board[row + dr][col + dc] == 'S' and 
                        self.board[row - dr][col - dc] == 'S'):
                        coordinates = [(row - dr, col - dc), (row, col), (row + dr, col + dc)]
                        return True, coordinates  # Return SOS coordinates
            
            # Check for the 'S' letter
            elif self.board[row][col] == 'S':
                if (0 <= row + 2 * dr < self.size and 0 <= col + 2 * dc < self.size):
                    # Check for SOS formation with 'O' in the middle
                    if (self.board[row + dr][col + dc] == 'O' and 
                        self.board[row + 2 * dr][col + 2 * dc] == 'S'):
                        coordinates = [(row, col), (row + dr, col + dc), (row + 2 * dr, col + 2 * dc)]
                        return True, coordinates  # Return SOS coordinates
        except IndexError:
            pass  # Ignore index errors due to boundary checks
    
        return False, None  # No SOS found

    def is_full(self):
        """Check if the board is full."""
        return all(self.board[row][col] != '' for row in range(self.size) for col in range(self.size))

    def check_winner_by_score(self):
        """Check if either player has reached a winning score."""
        if self.scores['Blue'] > self.scores['Red']:
            return 'Blue'  # Blue wins
        elif self.scores['Red'] > self.scores['Blue']:
            return 'Red'  # Red wins
        return None  # No winner

    def reset_game(self):
        """Reset the game board and scores for a new round."""
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]  # Clear the board
        self.scores = {'Blue': 0, 'Red': 0}  # Reset scores
        self.current_turn = random.choice(['Blue', 'Red'])  # Randomly choose starting player
        self.moves = []  # Reset moves for replay functionality
