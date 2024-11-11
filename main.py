import tkinter as tk
from src.ui import SOSGameUI
from src.game_logic import GameLogic

def main():
    root = tk.Tk()
    game_logic = GameLogic(3)  # Initialize the GameLogic object
    app = SOSGameUI(root, game_logic)  # Pass both root and game_logic
    root.mainloop()

if __name__ == "__main__":
    main()
