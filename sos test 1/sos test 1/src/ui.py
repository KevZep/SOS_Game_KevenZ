import tkinter as tk
from tkinter import messagebox
from src.game_logic import GameLogic

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
        self.record_var = tk.BooleanVar()
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

    def create_player_options(self, parent_frame, player_label, color):
        # Frame for each player's options
        player_frame = tk.Frame(parent_frame, bg="lightgray")
        player_frame.pack(anchor=tk.W, pady=5)

        # Player label
        tk.Label(player_frame, text=player_label, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=0, columnspan=3, sticky=tk.W)

        # Player choice for 'S' or 'O'
        if color == "Blue":
            self.blue_choice = tk.StringVar(value="S")  # Default choice for Blue
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.blue_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.blue_choice, value="O", bg="lightgray").grid(row=2, column=2)
        else:
            self.red_choice = tk.StringVar(value="S")  # Default choice for Red
            tk.Label(player_frame, text="Choose:", bg="lightgray").grid(row=2, column=0, pady=5)
            tk.Radiobutton(player_frame, text="S", variable=self.red_choice, value="S", bg="lightgray").grid(row=2, column=1)
            tk.Radiobutton(player_frame, text="O", variable=self.red_choice, value="O", bg="lightgray").grid(row=2, column=2)

    def start_game(self):
        # Start a new game based on the user input for size
        try:
            size_input = self.size_entry.get()
            size = int(size_input)  # Convert to integer

            # Validate size
            if size < 3 or size > 10:
                raise ValueError("Size must be between 3 and 10.")

            # Initialize game logic with selected mode and size
            self.game_logic = GameLogic(size, self.mode_var.get())  
            self.create_game_grid(size)  # Create the game grid
            self.update_turn_label()  # Update the turn label

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))  # Show error message for invalid input

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
        # Handle button click on the grid
        current_letter = self.blue_choice.get() if self.game_logic.current_turn == 'Blue' else self.red_choice.get()  # Determine current player's letter
        winner, sos_line = self.game_logic.place_letter(row, col, current_letter)  # Place letter and check for winner

        # Update the button text and disable it
        self.buttons[row][col].config(text=current_letter, state=tk.DISABLED)

        # Check for SOS and handle winner or draw logic
        if sos_line:  # Only color squares if an SOS was formed
            self.color_squares(sos_line)  # Color squares for the SOS

        if winner:
            self.update_scoreboard()  # Update scoreboard
            messagebox.showinfo("Game Over", f"{winner} wins!")  # Show winner message
            self.start_game()  # Reset the game for a new round
        elif self.game_logic.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")  # Show draw message
            self.start_game()  # Reset the game for a new round

        self.update_turn_label()  # Update turn label after processing
        self.update_scoreboard()  # Update scoreboard after processing


    def color_squares(self, sos_line):
        # Color the squares that formed the SOS
        if sos_line and len(sos_line) == 6:  # Ensure sos_line has correct length
            start_row, start_col, mid_row, mid_col, end_row, end_col = sos_line
            player_color = "lightblue" if self.game_logic.current_turn == 'Blue' else "red"

            # Change the color of the squares forming the SOS
            for r, c in [(start_row, start_col), (mid_row, mid_col), (end_row, end_col)]:
                button = self.buttons[r][c]
                button.config(bg=player_color)  # Change button background color
                current_letter = button["text"]
                button.config(font=("Arial", 12, "bold"), text=current_letter)  # Make text bold


    def update_turn_label(self):
        # Update the label to show whose turn it is
        self.turn_label.config(text=f"Current turn: {self.game_logic.current_turn}")  # Update turn display

    def update_scoreboard(self):
        # Update the scoreboard display
        scores = self.game_logic.scores  # Get current scores
        self.scoreboard.config(text=f"Blue: {scores['Blue']}  Red: {scores['Red']}")  # Update scoreboard label

    def replay_game(self):
        # Placeholder for replay functionality
        messagebox.showinfo("Replay", "Replay functionality is not implemented yet.")  # Inform that replay is not yet implemented

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    game_logic = GameLogic(3, "Simple")  # Initialize GameLogic with default values
    app = SOSGameUI(root, game_logic)  # Create an instance of SOSGameUI
    root.mainloop()  # Start the Tkinter event loop
