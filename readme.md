# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python, featuring singleplayer (vs. computer) and multiplayer modes, with automatic game saving and loading via JSON.

---

## Features

- **Singleplayer** — Play against a computer opponent that makes random moves
- **Multiplayer** — Play against another human on the same machine
- **Autosave** — The game automatically saves after every move to `savegame.json`
- **Load Game** — Resume a previously saved game from where you left off
- **Input Validation** — Handles invalid inputs, out-of-bounds moves, and occupied cells gracefully

---

## Requirements

- Python 3.x
- No external dependencies — uses only the Python standard library (`json`, `random`, `abc`)

---

## How to Run

```bash
python final_project.py
```

On launch, you'll be prompted to start a new game, load a saved game, or exit.

---

## Gameplay

- The board is a 3×3 grid. Rows and columns are numbered **0–2**.
- Player X always goes first.
- On your turn, enter the row and column number when prompted.
- The game ends when a player gets three in a row (horizontally, vertically, or diagonally), or the board fills up in a draw.

```
  |   |  
---------
  |   |  
---------
  |   |  
```

---

## Project Structure

```
tictactoe.py        # Main source file containing all classes and game logic
savegame.json       # Auto-generated save file (created after the first move)
```

### Key Classes

| Class | Responsibility |
|---|---|
| `Board` | Manages the grid, move placement, win/draw detection, and serialization |
| `Player` | Abstract base class defining the player interface |
| `HumanPlayer` | Handles human input and move placement |
| `ComputerPlayer` | Picks a random available cell each turn |
| `Game` | Drives gameplay, manages turn switching, saving, and loading |

---

## Save & Load

The game saves to `savegame.json` automatically after every move. To resume, select **Load Saved Game** from the main menu. If the saved game has already been won, loading is blocked and you'll be prompted to start a new game instead.

---

## Running Tests

```bash
python -m pytest test_final_project.py
```

The test suite uses `pytest` and covers the following:

**Board**
- Board initializes with all empty cells
- `place_mark` correctly places a mark on the grid
- `place_mark` raises `InvalidMoveError` for out-of-bounds moves
- `place_mark` raises `InvalidMoveError` when targeting an occupied cell
- `check_winner` detects wins by row, column, and diagonal
- `is_full` correctly returns `True` when all cells are filled and `False` when at least one is empty

**Player & Game**
- `switch_player` correctly alternates between Player 1 and Player 2
- `check_winner` detects a winner through the `Game` object's board
- Draw state is correctly identified when the board is full with no winner

---

## Possible Future Improvements

- Score tracking across multiple rounds
- Configurable board size