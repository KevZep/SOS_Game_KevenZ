import tkinter as tk
from tkinter import messagebox
from src.game_logic import GameLogic
import random
import os

class SOSGameUI:
    def __init__(self, root, game_logic):
        self.root = root  # Store the root window
        self.game_logic = game_logic  # Initialize game logic
        self.buttons = []  # List to store grid buttons
        self.create_ui()  # Create the UI components

    def create_ui(self):
        self.root.title("SOS Game")  # Set the window title

        # Main Frame
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="lightgray")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        title_label = tk.Label(main_frame, text="SOS Game", font=("Arial", 20, "bold"), bg="lightgray")
        title_label.pack(pady=10)

        # Game Mode and Size Frame
        mode_size_frame = tk.Frame(main_frame, bg="lightgray")
        mode_size_frame.pack(pady=10)

        # Game Mode Selection
        tk.Label(mode_size_frame, text="Game Mode:", bg="lightgray").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="Simple")  # Default mode
        tk.Radiobutton(mode_size_frame, text="Simple", variable=self.mode_var, value="Simple", bg="lightgray", command=self.on_mode_change).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(mode_size_frame, text="General", variable=self.mode_var, value="General", bg="lightgray", command=self.on_mode_change).grid(row=0, column=2, sticky=tk.W)

        # Size Entry
        tk.Label(mode_size_frame, text="Size:", bg="lightgray").grid(row=0, column=3, sticky=tk.W)
        self.size_entry = tk.Entry(mode_size_frame, width=5)
        self.size_entry.grid(row=0, column=4)

        # Grid Frame
        self.grid_frame = tk.Frame(main_frame, bg="lightgray")
        self.grid_frame.pack(pady=10)

        # Player Options Frame
        options_frame = tk.Frame(main_frame, bg="lightgray")
        options_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create options for each player
        self.create_player_options(options_frame, "Blue Player", "Blue")
        self.create_player_options(options_frame, "Red Player", "Red")

        # Control Buttons Frame
        control_frame = tk.Frame(main_frame, bg="lightgray")
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Record Game Checkbox
        self.record_var = tk.BooleanVar(value=False)  # Initialize with False
        tk.Checkbutton(control_frame, text="Record Game", variable=self.record_var, bg="lightgray").pack(side=tk.LEFT)

        # Control Buttons
        tk.Button(control_frame, text="Replay", command=self.replay_game).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="New Game", command=self.start_game).pack(side=tk.LEFT, padx=5)

        # Current Turn Label
        self.turn_label = tk.Label(main_frame, text=f"Current turn: {self.game_logic.current_turn}", bg="lightgray")
        self.turn_label.pack(side=tk.BOTTOM, pady=10)

        # Scoreboard
        self.scoreboard = tk.Label(main_frame, text=f"Blue: 0  Red: 0", bg="lightgray", font=("Arial", 12, "bold"))
        self.scoreboard.pack(side=tk.BOTTOM, pady=5)

        self.blue_is_ai = tk.BooleanVar()
        self.red_is_ai = tk.BooleanVar()

        # Add checkboxes for AI players
        #tk.Checkbutton(player_frame, text="Blue AI", variable=self.blue_is_ai).grid(row=0, column=2)
        #tk.Checkbutton(player_frame, text="Red AI", variable=self.red_is_ai).grid(row=1, column=2)


    def create_player_options(self, parent_frame, player_label, color):
        player_frame = tk.Frame(parent_frame, bg="lightgray")
        player_frame.pack(anchor=tk.W, pady=5)

        tk.Label(player_frame, text=player_label, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=0, columnspan=3, sticky=tk.W)

        if color == "Blue":
            # Player type selection for Blue
            self.blue_type = tk.StringVar(value="Human")
            tk.Label(player_frame, text="Player Type:", bg="lightgray").grid(row=1, column=0, pady=5)
            tk.Radiobutton(player_frame, text="Human", variable=self.blue_type, value="Human", bg="lightgray").grid(row=1, column=1)
            tk.Radiobutton(player_frame, text="Computer", variable=self.blue_type, value="Computer", bg="lightgray").grid(row=1, column=2)

            # Blue player choice for 'S' or 'O'
            self.blue_choice = tk.StringVar(value="S")
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.blue_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.blue_choice, value="O", bg="lightgray").grid(row=2, column=2)
        else:
            # Player type selection for Red
            self.red_type = tk.StringVar(value="Human")
            tk.Label(player_frame, text="Player Type:", bg="lightgray").grid(row=1, column=0, pady=5)
            tk.Radiobutton(player_frame, text="Human", variable=self.red_type, value="Human", bg="lightgray").grid(row=1, column=1)
            tk.Radiobutton(player_frame, text="Computer", variable=self.red_type, value="Computer", bg="lightgray").grid(row=1, column=2)

            # Red player choice for 'S' or 'O'
            self.red_choice = tk.StringVar(value="S")
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.red_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.red_choice, value="O", bg="lightgray").grid(row=2, column=2)

    def start_game(self, is_replay=False):
        try:
            size_input = self.size_entry.get()
            size = int(size_input)
            if size < 3 or size > 10:
                raise ValueError("Size must be between 3 and 10.")
        
            # Clear existing record file only when starting a new game and not replaying
            if self.record_var.get() and not is_replay:
                open("game_record.txt", "w").close()

            self.game_logic = GameLogic(size, self.mode_var.get())
            self.create_game_grid(size)
            self.update_turn_label()
            self.update_scoreboard()
        
            # Check if the first player is a computer and make a move only if not replaying
            if not is_replay and ((self.game_logic.current_turn == 'Blue' and self.blue_type.get() == "Computer") or 
                                  (self.game_logic.current_turn == 'Red' and self.red_type.get() == "Computer")):
                self.root.after(500, self.ai_turn)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def on_mode_change(self):
        # Handle game mode change
        if messagebox.askyesno("Change Mode", "Changing the game mode will reset the score and hide the board. Do you want to continue?"):
            self.game_logic.scores = {'Blue': 0, 'Red': 0}  # Reset scores
            self.start_game()  # Restart the game

    def create_game_grid(self, size):
        # Create the grid based on the specified size
        for widget in self.grid_frame.winfo_children():
            widget.destroy()  # Clear the previous grid

        self.buttons = []  # Reset button list
        for r in range(size):
            row = []
            for c in range(size):
                # Create a button for each cell in the grid
                btn = tk.Button(self.grid_frame, text="", width=5, height=2, 
                                font=("Arial", 12), command=lambda r=r, c=c: self.on_grid_click(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)  # Place button in grid
                row.append(btn)
            self.buttons.append(row)  # Append row to buttons list
        self.grid_frame.pack()  # Display the grid

    def on_grid_click(self, row, col):
        current_letter = self.blue_choice.get() if self.game_logic.current_turn == 'Blue' else self.red_choice.get()
        winner, sos_line = self.game_logic.place_letter(row, col, current_letter)

        self.record_move(row, col, current_letter)
        self.buttons[row][col].config(text=current_letter, state=tk.DISABLED)

        if sos_line:
            self.color_squares(sos_line)

        if winner:
            self.update_scoreboard()
            self.end_game_dialog(f"{winner} wins!")
        elif self.game_logic.is_full():
            self.end_game_dialog("It's a draw!")
        else:
            self.update_turn_label()
            self.update_scoreboard()

            if (self.game_logic.current_turn == 'Blue' and self.blue_type.get() == "Computer") or \
               (self.game_logic.current_turn == 'Red' and self.red_type.get() == "Computer"):
                self.root.after(500, self.ai_turn)

    def handle_move_result(self, winner, sos_line):
        # Handle SOS coloring and end-game messages
        if sos_line:
            self.color_squares(sos_line)

        if winner:
            self.update_scoreboard()
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.start_game()  # Restart for a new round
        elif self.game_logic.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.start_game()
        else:
            # Update turn label and scoreboard after each move
            self.update_turn_label()
            self.update_scoreboard()

            # Check for AI turn
            self.check_ai_turn()

    def ai_turn(self):
        row, col, letter = self.game_logic.ai_move()
        if row is not None and col is not None:
            self.buttons[row][col].config(text=letter, state=tk.DISABLED)
            winner, sos_line = self.game_logic.place_letter(row, col, letter)
            self.record_move(row, col, letter)

            if sos_line:
                self.color_squares(sos_line)

            if winner:
                self.update_scoreboard()
                self.end_game_dialog(f"{winner} wins!")
            elif self.game_logic.is_full():
                self.end_game_dialog("It's a draw!")
            else:
                self.update_turn_label()
                self.update_scoreboard()
                self.check_ai_turn()

    def color_squares(self, sos_line):
        print(f"Coloring SOS line: {sos_line}")
        if sos_line:
            player_color = "lightblue" if self.game_logic.current_turn == 'Blue' else "#FFB6C1"
            for sos in sos_line:
                for row, col in sos:
                    button = self.buttons[row][col]

                    current_color = button.cget('bg')
                    if current_color in ["lightblue", "#FFB6C1", "#CBC3E3"]:
                        player_color = "#CBC3E3"
                    else:
                        player_color = player_color

                    button.config(bg=player_color)  # Change background color
                    current_letter = button["text"]
                    button.config(font=("Arial", 12, "bold"))
                    print(f"Colored button at ({row}, {col}) to {player_color}")


    def handle_move_result(self, winner, sos_line):
        if sos_line:
            self.color_squares(sos_line)
        if winner:
            self.update_scoreboard()
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.start_game()
        elif self.game_logic.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.start_game()
        else:
            self.update_turn_label()
            self.update_scoreboard()
            self.check_ai_turn()
    
    def check_ai_turn(self):
        if (self.game_logic.current_turn == 'Blue' and self.blue_type.get() == "Computer") or \
           (self.game_logic.current_turn == 'Red' and self.red_type.get() == "Computer"):
            self.root.after(500, self.ai_turn)  # Delay for AI response

    def update_turn_label(self):
        # Update the label to show whose turn it is
        self.turn_label.config(text=f"Current turn: {self.game_logic.current_turn}")  # Update turn display

    def update_scoreboard(self):
        # Update the scoreboard display
        scores = self.game_logic.scores  # Get current scores
        self.scoreboard.config(text=f"Blue: {scores['Blue']}  Red: {scores['Red']}")  # Update scoreboard label

    def replay_game(self):
        print("Replay button clicked")
        if not os.path.exists("game_record.txt"):
            messagebox.showerror("Error", "No recorded game found.")
            return

        print("Game record file found")
        self.start_game(is_replay=True)  # Reset the game board for replay
        with open("game_record.txt", "r") as file:
            moves = file.readlines()
    
        print(f"Loaded {len(moves)} moves")

        # Reset scores for replay
        self.game_logic.scores = {'Blue': 0, 'Red': 0}

        def play_move(move_index):
            if move_index < len(moves):
                turn, letter, row, col = moves[move_index].strip().split(',')
                row, col = int(row), int(col)
                print(f"Playing move: {turn} places {letter} at ({row}, {col})")
            
                # Place the letter without applying game rules
                self.game_logic.board[row][col] = letter
                self.buttons[row][col].config(text=letter, state=tk.DISABLED)
            
                # Check for SOS formations
                sos_list = self.game_logic.check_for_sos(row, col, letter)
                if sos_list:
                    self.game_logic.scores[turn] += len(sos_list)
                    self.color_squares(sos_list)
            
                self.game_logic.current_turn = turn
                self.update_turn_label()
                self.update_scoreboard()
                self.root.after(1000, play_move, move_index + 1)  # Play next move after 1 second
            else:
                winner = self.game_logic.check_winner_by_score()
                messagebox.showinfo("Replay Finished", f"The replay has finished. Winner: {winner}")

        play_move(0)

    def end_game_dialog(self, message):
        result = messagebox.askquestion("Game Over", f"{message}\n\nDo you want to start a new game?", 
                                        icon='info', type='yesno')
        if result == 'yes':
            self.start_game()
        # If 'no', do nothing and let the user change settings if desired

    def record_move(self, row, col, letter):
        if self.record_var.get():
            with open("game_record.txt", "a") as file:
                move = f"{self.game_logic.current_turn},{letter},{row},{col}\n"
                file.write(move)
                print(f"Recorded move: {move.strip()}")  # Add this line

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    game_logic = GameLogic(3, "Simple")  # Initialize GameLogic with default values
    app = SOSGameUI(root, game_logic)  # Create an instance of SOSGameUI
    root.mainloop()  # Start the Tkinter event loop
