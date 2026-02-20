import json
import random
from abc import ABC, abstractmethod

class InvalidMoveError(Exception):
    """Raised when a move is invalid."""
    pass

class Board:
    """Handles all board-related functionalities.
    Creates the board, allows user to place marks on the board.
    Checks if board is full, or if there is a winner.
    Has functionality for dictionary conversion to enable serialization."""

    size = 3

    def __init__(self):
        """
        List comprehension used for brevity. 
        The inner loop adds " " to the list 3 times to create a row, 
        and the outer loop repeats row creation 3 times to make the grid.
        """
        self._grid = [[" " for board_space in range(self.size)] for board_space in range(self.size)]

    @property
    def grid(self):
        return self._grid

    def place_mark(self, row, col, mark):
        """Places mark on the board."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise InvalidMoveError("Move out of bounds.")
        if self._grid[row][col] != " ":
            raise InvalidMoveError("Cell already taken.")
        self._grid[row][col] = mark

    def check_winner(self):
        """Checks if there is a winner by looking for all-matching rows, columns and diagonals."""

        # Rows
        for row in self._grid:
            # if first cell in row not blank (meaning row isn't blank) and rows all equal
            if row[0] != " " and row[0] == row[1] == row[2]:
                return row[0]

        # Columns
        for col in range(self.size):
            # if top cell is not blank (meaning column isnt blank) and columns all equal
            if self._grid[0][col] != " " and self._grid[0][col] == self._grid[1][col] == self._grid[2][col]:
                return self._grid[0][col]

        # Diagonals
        if self._grid[0][0] != " " and self._grid[0][0] == self._grid[1][1] == self._grid[2][2]:
            return self._grid[0][0]
        if self._grid[0][2] != " " and self._grid[0][2] == self._grid[1][1] == self._grid[2][0]:
            return self._grid[0][2]

        return None # no winner yet, game keeps going until one of the above conditions is met

    def is_full(self):
        """Checks if board is full."""
        for row in self._grid:
            for cell in row:
                if cell == " ":
                    return False
        return True # if no blank spots, then full

    def __str__(self):
        """Returns board visual output so it doesn't return a memory address."""
        lines = []
        for row in self._grid:
            lines.append(" | ".join(row)) # "|" symbol added between each row's cells
        return "\n---------\n".join(lines) # dashes added between each element in lines (meaning, each row)

    # JSON SERIALIZATION - DICTIONARY CONVERSION
    def to_dict(self):
        """Convert to dictionary to enable autosave functionalities.
        JSON cannot read board directly, so conversion necessary."""
        return {"grid": self._grid}

    @classmethod
    def from_dict(cls, data):
        """Get data from dictionary."""
        board = cls() # creates an instance of whatever class the method is being called on
        board._grid = data["grid"] # replaces default grid with the saved grid from dictionary
        return board

# PLAYER CLASSES
class Player(ABC):
    """Initializes name and mark, and forces subclasses to create make_move methods."""
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    @abstractmethod
    def make_move(self, board):
        """Forces HumanPlayer and ComputerPlayer into having
        their own specific make_move functions."""
        pass

class HumanPlayer(Player): # Inheritance
    """Represents a human player and their ability to make a move on the board."""
    def make_move(self, board):
        """Allows the human player to add a mark on the board at their desired spot."""
        while True:
            try:
                row = int(input(f"{self.name} ({self.mark}) - Enter row (0-2): "))
                col = int(input(f"{self.name} ({self.mark}) - Enter column (0-2): "))
                board.place_mark(row, col, self.mark)
                break
            except ValueError:
                print("Invalid input. Please enter numbers.")
            except InvalidMoveError as e: # Error if cell occupied or out of bounds
                print("Error:", e)

class ComputerPlayer(Player): # Inheritance
    """Represents a computer player and their ability to make a move on the board at random."""
    def make_move(self, board):
        """Adds all current blank cells on the board to a list,
        which the computer uses as a reference to find where
        it can place a mark at random."""

        print(f"\n{self.name} ({self.mark}) is making a move...")
        empty_cells = []
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == " ": # grid property used here
                    empty_cells.append((row, col))

        # Choose random empty cell
        row, col = random.choice(empty_cells)
        board.place_mark(row, col, self.mark)

# GAME CLASS
class Game:
    """Has functionalities for player-switching, and drives gameplay. Allows for autosave and loading."""
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_index = 0

    @property
    def current_player(self):
        """Looks at the current index to see whose turn it is."""
        return self.players[self.current_index]

    def switch_player(self):
        """Switches player every turn. If 1, then 1-1=0. If 0, then 1-0=1."""
        self.current_index = 1 - self.current_index

    def play(self):
        """Main gameplay-driving function.
        Prints board, lets the current player make move, then autosaves.
        Checks for winners, or if board is full, and gives a result accordingly."""
        while True:
            print("\n" + str(self.board)) # __str__ used here to print board
            self.current_player.make_move(self.board)

            # auto-save after every move
            self.save("savegame.json")

            winner = self.board.check_winner()
            if winner:
                print("\n" + str(self.board)) # prints final board
                print(f"\n{self.current_player.name} wins!")
                break

            if self.board.is_full():
                print("\n" + str(self.board)) # prints final board
                print("\nIt's a draw!")
                break

            self.switch_player()


    # JSON SERIALIZATION - AUTOSAVE
    def save(self, filename):
        """Saves data to json. Saves in dictionary format."""
        data = {
            "board": self.board.to_dict(),
            "players": [
                {"name": p.name, "mark": p.mark, "type": p.__class__.__name__}
                for p in self.players
            ],
            "current_index": self.current_index
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, filename):
        """Loads data from json. Checks if computer or human, and appends accordingly."""
        with open(filename, "r") as f:
            data = json.load(f)

        players = []
        for player_data in data["players"]: # checks for player data within the json
            if player_data.get("type") == "ComputerPlayer":
                players.append(ComputerPlayer(player_data["name"], player_data["mark"]))
            else:
                players.append(HumanPlayer(player_data["name"], player_data["mark"]))

        # initializes new game object with the two players
        game = cls(players[0], players[1])
        game.board = Board.from_dict(data["board"])
        game.current_index = data["current_index"]

        # checks if saved game has already been won by a player, prevents loading
        winner = game.board.check_winner()
        if winner:
            raise ValueError(f"Cannot load saved game: {winner} has already won!")
        return game

# MAIN

if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe!")

    while True:
        choice = ""
        while choice != "1" and choice != "2" and choice != "3":
            choice = input(
                "\nSelect option:\n"
                "1. New Game\n"
                "2. Load Saved Game\n"
                "3. Exit\n"
                "Enter 1, 2 or 3: "
            )

        if choice == "1":
            mode = ""
            while mode != "1" and mode != "2":
                mode = input(
                    "\nSelect mode:\n"
                    "1. Singleplayer (vs Computer)\n"
                    "2. Multiplayer (2 Humans)\n"
                    "Enter 1 or 2: "
                )

            if mode == "1":
                p1 = HumanPlayer("Player", "X")
                p2 = ComputerPlayer("Computer", "O")
            else:
                p1 = HumanPlayer("Player 1", "X")
                p2 = HumanPlayer("Player 2", "O")

            game = Game(p1, p2)

        elif choice == "2":
            try:
                game = Game.load("savegame.json")
                print("\nLoaded saved game successfully!")
            except FileNotFoundError:
                print("\nNo saved game found. Please choose to start a new game, or exit if you wish.")
                continue
            except ValueError as e:
                print("\n" + str(e))
                print("Please choose to start a new game instead, or exit if you wish.")
                continue

        else:
            print("Exiting the game...")
            break

        game.play()

        # Ask to play again
        while True:
            again = input("\nDo you want to play another game? (yes/no): ").strip().lower()
            if again in ["yes", "no"]:
                break
            print("\nPlease enter 'yes' for yes or 'no' for no.")

        if again == "no":
            print("\nThanks for playing!")
            break
