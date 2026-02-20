import pytest
from final_project import Board, Game, HumanPlayer, InvalidMoveError

# BOARD TEST

def test_board_starts_empty():
    board = Board()
    for row in board.grid:
        assert row == [" ", " ", " "]

def test_place_mark_works():
    board = Board()
    board.place_mark(0, 0, "X")
    assert board.grid[0][0] == "X"

def test_place_mark_out_of_bounds_raises():
    board = Board()
    with pytest.raises(InvalidMoveError):
        board.place_mark(3, 0, "X")

def test_mark_on_taken_cell_raises_error():
    board = Board()
    board.place_mark(0, 0, "X")
    with pytest.raises(InvalidMoveError):
        board.place_mark(0, 0, "O")

def test_check_winner_row():
    board = Board()
    board._grid = [["X","X","X"], [" ","O"," "], ["O"," "," "]]
    assert board.check_winner() == "X"

def test_check_winner_column():
    board = Board()
    board._grid = [["O","X"," "], ["O","X"," "], ["O"," ","X"]]
    assert board.check_winner() == "O"

def test_check_winner_diagonal():
    board = Board()
    board._grid = [["X","O","O"], ["O","X"," "], [" "," ","X"]]
    assert board.check_winner() == "X"

def test_board_is_full_true():
    board = Board()
    board._grid = [["X","O","X"], ["O","X","O"], ["O","X","O"]]
    assert board.is_full() is True

def test_board_is_full_false():
    board = Board()
    board._grid = [["X","O"," "], ["O","X","O"], ["O","X","O"]]
    assert board.is_full() is False

# PLAYER AND GAME TEST

def test_switch_player_changes_current():
    p1 = HumanPlayer("A","X")
    p2 = HumanPlayer("B","O")
    game = Game(p1,p2)
    assert game.current_player == p1
    game.switch_player()
    assert game.current_player == p2

def test_game_winner_detection():
    p1 = HumanPlayer("A","X")
    p2 = HumanPlayer("B","O")
    game = Game(p1,p2)
    game.board._grid = [["X","X","X"], ["O"," "," "], ["O"," "," "]]
    assert game.board.check_winner() == "X"

def test_game_draw_detection():
    p1 = HumanPlayer("A","X")
    p2 = HumanPlayer("B","O")
    game = Game(p1,p2)
    game.board._grid = [["X","O","X"], ["X","O","O"], ["O","X","X"]]
    assert game.board.check_winner() is None
    assert game.board.is_full() is True
