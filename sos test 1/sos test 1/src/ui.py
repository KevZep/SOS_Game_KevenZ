import tkinter as tk
from tkinter import messagebox
from src.game_logic import GameLogic

class SOSGameUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game_logic = game_logic  # Initialize with game logic
        self.buttons = []  # To hold the grid buttons
        self.create_ui()

    def create_ui(self):
        self.root.title("SOS Game")
        
        # Main Frame
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="lightgray")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        title_label = tk.Label(main_frame, text="SOS Game", font=("Arial", 20, "bold"), bg="lightgray")
        title_label.pack(pady=10)

        # Game Mode and Size Frame
        mode_size_frame = tk.Frame(main_frame, bg="lightgray")
        mode_size_frame.pack(pady=10)

        tk.Label(mode_size_frame, text="Game Mode:", bg="lightgray").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(mode_size_frame, text="Simple", value="Simple", bg="lightgray").grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(mode_size_frame, text="General", value="General", bg="lightgray").grid(row=0, column=2, sticky=tk.W)
        tk.Label(mode_size_frame, text="Size:", bg="lightgray").grid(row=0, column=3, sticky=tk.W)
        self.size_entry = tk.Entry(mode_size_frame, width=5)
        self.size_entry.grid(row=0, column=4)

        # Grid Frame
        self.grid_frame = tk.Frame(main_frame, bg="lightgray")
        self.grid_frame.pack(pady=10)

        # Player Options Frame
        options_frame = tk.Frame(main_frame, bg="lightgray")
        options_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.create_player_options(options_frame, "Blue Player", "Blue")
        self.create_player_options(options_frame, "Red Player", "Red")

        # Control Buttons Frame
        control_frame = tk.Frame(main_frame, bg="lightgray")
        control_frame.pack(side=tk.BOTTOM, pady=10)

        self.record_var = tk.BooleanVar()
        tk.Checkbutton(control_frame, text="Record Game", variable=self.record_var, bg="lightgray").pack(side=tk.LEFT)

        tk.Button(control_frame, text="Replay", command=self.replay_game).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="New Game", command=self.start_game).pack(side=tk.LEFT, padx=5)

        # Current Turn Label
        self.turn_label = tk.Label(main_frame, text="Current turn: Blue", bg="lightgray")
        self.turn_label.pack(side=tk.BOTTOM, pady=10)

    def create_player_options(self, parent_frame, player_label, color):
        player_frame = tk.Frame(parent_frame, bg="lightgray")
        player_frame.pack(anchor=tk.W, pady=5)

        tk.Label(player_frame, text=player_label, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=0, columnspan=3, sticky=tk.W)

        if color == "Blue":
            self.blue_choice = tk.StringVar(value="S")
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.blue_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.blue_choice, value="O", bg="lightgray").grid(row=2, column=2)
        else:
            self.red_choice = tk.StringVar(value="S")
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.red_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.red_choice, value="O", bg="lightgray").grid(row=2, column=2)

    def start_game(self):
        try:
            size_input = self.size_entry.get()
            size = int(size_input)  # Convert to integer
    
            if size < 3 or size > 10:
                raise ValueError("Size must be between 3 and 10.")
    
            self.game_logic = GameLogic(size)  # Create the game logic
            self.create_game_grid(size)  # Create the game grid
            self.turn_label.config(text=f"Current turn: {self.game_logic.current_turn}")  # Set the starting turn

        except ValueError as e:
            messagebox.showerror("Invalid Size", str(e))


    def create_game_grid(self, size):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()  # Clear the existing grid

        self.buttons = []  # Reset button list

        # Create buttons for the grid
        for row in range(size):
            row_buttons = []
            for col in range(size):
                button = tk.Button(self.grid_frame, text='', width=5, height=2,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def make_move(self, row, col):
        current_letter = self.get_player_choice()  # Get current player's letter choice
        print(f"{self.game_logic.current_turn} is making a move: {current_letter}")

        winner = self.game_logic.place_letter(row, col, current_letter)  # Pass the chosen letter

        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col].config(text=current_letter, state="disabled")  # Disable button after move

            if winner:
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.reset_game()
            elif self.game_logic.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.game_logic.current_turn
                #self.update_turn()  # Update the turn if no one has won or drawn


    def get_player_choice(self):
        if self.game_logic.current_turn == 'Blue':
            return self.blue_choice.get()  # Get Blue player's choice (S or O)
        else:
            return self.red_choice.get()  # Get Red player's choice (S or O)

    def reset_game(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(text='', state="normal")  # Clear buttons and re-enable
        self.blue_choice.set("S")  # Reset player choices if needed
        self.red_choice.set("S")
        self.game_logic = GameLogic(self.game_logic.grid_size)  # Restart the game logic with the same grid size
        #self.update_turn()  # Update to show the starting turn

    #def reset_game(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(text='', state="normal")  # Clear and re-enable buttons
        self.blue_choice.set("S")
        self.red_choice.set("S")
        self.game_logic = GameLogic(self.game_logic.grid_size)
        #self.update_turn()

    def replay_game(self):
        self.reset_game()

    def update_turn(self):
        # Toggle current turn
        print(f"Current turn before updating: {self.game_logic.current_turn}")
        self.game_logic.current_turn = self.game_logic.current_turn #'Red' if self.game_logic.current_turn == 'Blue' else 'Blue'
        # Update the UI label to show the current turn
        print(f"Current turn after updating: {self.game_logic.current_turn}")
        self.turn_label.config(text=f"Current turn: {self.game_logic.current_turn}")

    #def update_turn(self):
        current_turn_color = self.game_logic.current_turn  # Get current turn color
        print(f"Updating turn from {current_turn_color}")  # Debugging output

        # Determine the next turn
        next_turn = 'Red' if current_turn_color == 'Blue' else 'Blue'
        self.turn_label.config(text=f"Current turn: {next_turn}")

        self.game_logic.current_turn = next_turn  # Change the turn in game logic
        print(f"Turn updated to {next_turn}")

