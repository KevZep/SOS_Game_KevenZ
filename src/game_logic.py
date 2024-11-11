import random

class GameLogic:
    def __init__(self, size, mode='Simple'):
        self.size = size
        self.mode = mode
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_turn = random.choice(['Blue', 'Red'])
        self.scores = {'Blue': 0, 'Red': 0}
        self.moves = []
        print(f"Game initialized: Size {size}, Mode {mode}")
        print(f"Starting player: {self.current_turn}")

    def place_letter(self, row, col, letter):
        print(f"{self.current_turn}'s turn. Trying to place {letter} at ({row}, {col}).")
        if self.board[row][col] == '':
            self.board[row][col] = letter
            self.moves.append((row, col, letter, self.current_turn))
            print(f"Placed {letter} at ({row}, {col}) by {self.current_turn}.")
            sos_list = self.check_for_sos(row, col, letter)
            
            if sos_list:
                self.scores[self.current_turn] += len(sos_list)
                print(f"{self.current_turn} formed SOS at {sos_list}. Current score: {self.scores[self.current_turn]}")
                if self.mode == 'Simple':
                    print(f"{self.current_turn} wins the game in Simple mode.")
                    return self.current_turn, sos_list
                elif self.mode == 'General':
                    if self.is_full():
                        winner = self.check_winner_by_score()
                        print(f"{winner} wins the game in General mode with a score of {self.scores[winner]}.")
                        return winner, sos_list
                    print(f"{self.current_turn} will take another turn for making SOS.")
                    return None, sos_list
            
            self.switch_turn()
            print(f"Next turn: {self.current_turn}")
            if self.is_full():
                if self.mode == 'Simple':
                    print(f"(DRAW)")
                else:
                    winner = self.check_winner_by_score()
                    print(f"{winner} wins the game in General mode with a score of {self.scores[winner]}.")
                    return winner, None
            return None, None
        print(f"Failed to place {letter} at ({row}, {col}). Cell already occupied.")
        return None, None

    def check_for_sos(self, row, col, letter):
        print(f"Checking for SOS formations at ({row}, {col}) with letter {letter}.")
        if self.mode == 'Simple':
            return self.check_simple_sos(row, col, letter)
        elif self.mode == 'General':
            return self.check_general_sos(row, col, letter)

    def check_simple_sos(self, row, col, letter):
        sos_found, coordinates = self.is_sos(row, col)
        if sos_found:
            print(f"SOS found in Simple mode at {coordinates}.")
            return [coordinates]
        return None

    def check_general_sos(self, row, col, letter):
        sos_list = []
        checked_positions = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            sos_found, coordinates = self.is_sos_in_direction(row, col, dr, dc)
            if sos_found:
                coord_set = frozenset(coordinates)
                if coord_set not in checked_positions:
                    sos_list.append(coordinates)
                    checked_positions.add(coord_set)
        if sos_list:
            print(f"SOS found in General mode at {sos_list}.")
        return sos_list if sos_list else None

    def is_sos(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            sos_found, coordinates = self.is_sos_in_direction(row, col, dr, dc)
            if sos_found:
                return True, coordinates
        return False, None

    def is_sos_in_direction(self, row, col, dr, dc):
        try:
            if self.board[row][col] == 'O':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row - dr < self.size and 0 <= col - dc < self.size):
                    if (self.board[row + dr][col + dc] == 'S' and
                        self.board[row - dr][col - dc] == 'S'):
                        return True, [(row - dr, col - dc), (row, col), (row + dr, col + dc)]
            elif self.board[row][col] == 'S':
                if (0 <= row + 2 * dr < self.size and 0 <= col + 2 * dc < self.size):
                    if (self.board[row + dr][col + dc] == 'O' and
                        self.board[row + 2 * dr][col + 2 * dc] == 'S'):
                        return True, [(row, col), (row + dr, col + dc), (row + 2 * dr, col + 2 * dc)]
        except IndexError:
            pass
        return False, None

    def is_full(self):
        full = all(self.board[r][c] != '' for r in range(self.size) for c in range(self.size))
        if full:
            print("The board is full.")
        return full

    def check_winner_by_score(self):
        if self.scores['Blue'] > self.scores['Red']:
            return 'Blue'
        elif self.scores['Red'] > self.scores['Blue']:
            return 'Red'
        print("The game is a draw.")
        return 'Draw'

    def switch_turn(self):
        self.current_turn = 'Red' if self.current_turn == 'Blue' else 'Blue'
        print(f"Switched turn to {self.current_turn}")

    def ai_move(self):
        print("AI is making a move...")
        for letter in ['S', 'O']:
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == '':
                        if self.completes_sos(row, col, letter):
                            print(f"AI completes SOS with {letter} at ({row}, {col})")
                            return row, col, letter
        
        for letter in ['S', 'O']:
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == '':
                        if self.sets_up_sos(row, col, letter):
                            print(f"AI sets up SOS with {letter} at ({row}, {col})")
                            return row, col, letter
        
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            letter = random.choice(['S', 'O'])
            print(f"AI makes a random move with {letter} at ({row}, {col})")
            return row, col, letter
        
        print("AI couldn't make a move")
        return None, None, None

    def completes_sos(self, row, col, letter):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            if letter == 'S':
                if (0 <= row + 2*dr < self.size and 0 <= col + 2*dc < self.size and
                    self.board[row + dr][col + dc] == 'O' and
                    self.board[row + 2*dr][col + 2*dc] == 'S'):
                    return True
            elif letter == 'O':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row - dr < self.size and 0 <= col - dc < self.size and
                    self.board[row + dr][col + dc] == 'S' and
                    self.board[row - dr][col - dc] == 'S'):
                    return True
        return False

    def sets_up_sos(self, row, col, letter):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            if letter == 'S':
                if (0 <= row + 2*dr < self.size and 0 <= col + 2*dc < self.size and
                    self.board[row + dr][col + dc] == 'O' and
                    self.board[row + 2*dr][col + 2*dc] == ''):
                    return True
                if (0 <= row + 2*dr < self.size and 0 <= col + 2*dc < self.size and
                    self.board[row + dr][col + dc] == '' and
                    self.board[row + 2*dr][col + 2*dc] == 'S'):
                    return True
            elif letter == 'O':
                if (0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    0 <= row - dr < self.size and 0 <= col - dc < self.size and
                    ((self.board[row + dr][col + dc] == 'S' and self.board[row - dr][col - dc] == '') or
                     (self.board[row + dr][col + dc] == '' and self.board[row - dr][col - dc] == 'S'))):
                    return True
        return False