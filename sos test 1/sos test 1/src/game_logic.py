import random

class GameLogic:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        #self.current_turn = 'Blue'  # Ensure this starts as Blue
        self.blue_choice = 'S'  # Default choice for Blue
        self.red_choice = 'S'  # Default choice for Red
        self.current_turn = random.choice(['Blue', 'Red'])  # Randomly choose the starting player

    def place_letter(self, row, col, letter):
        print(f"Attempting to place {letter} at ({row}, {col}) by {self.current_turn}")
        
        if self.grid[row][col] == '':
            self.grid[row][col] = letter  # Place the chosen letter
            print(f"Placed {letter} at ({row}, {col})")
            
            if self.check_sos(row, col):  # Check for "SOS"
                print(f"{self.current_turn} has formed an SOS!")
                return self.current_turn  # Return the winner (current player)
            
            # Switch turn after a successful move
            self.current_turn = 'Red' if self.current_turn == 'Blue' else 'Blue'
            print(f"Turn changed to {self.current_turn}")
        else:
            print("Cell already occupied.")
        return None


    def check_sos(self, row, col):
        return (
            self.check_sos_in_direction(row, col, 0, 1) or  # Horizontal
            self.check_sos_in_direction(row, col, 1, 0) or  # Vertical
            self.check_sos_in_direction(row, col, 1, 1) or  # Diagonal \
            self.check_sos_in_direction(row, col, 1, -1)    # Diagonal /
        )

    def check_sos_in_direction(self, row, col, delta_row, delta_col):
        line = []
        for d in range(-2, 3):  # Iterate from -2 to 2 to cover all possible 'SOS' directions
            r, c = row + d * delta_row, col + d * delta_col
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                line.append(self.grid[r][c])  # Collect characters
            if len(line) == 3:  # Only check when we have a 3-character sequence
                if "".join(line) == "SOS":
                    return True
                line.pop(0)  # Remove the first character to keep the sliding window of 3
        return False


    def is_full(self):
        return all(cell != '' for row in self.grid for cell in row)
