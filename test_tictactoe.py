import unittest

from tictactoe import (
    new_board,
    is_valid_move,
    make_move,
    check_winner,
    is_draw,
    computer_move,
    parse_position,
)


def board_from(s):
    """Build a board from a 9-character string, '.' for empty, e.g. 'XXX......'."""
    return [c if c != "." else " " for c in s]


class TestBoardBasics(unittest.TestCase):
    def test_new_board_is_nine_empty_cells(self):
        self.assertEqual(new_board(), [" "] * 9)

    def test_valid_move_on_empty_cell(self):
        self.assertTrue(is_valid_move(new_board(), 5))

    def test_invalid_move_on_taken_cell(self):
        board = make_move(new_board(), 5, "X")
        self.assertFalse(is_valid_move(board, 5))

    def test_invalid_move_out_of_range(self):
        self.assertFalse(is_valid_move(new_board(), 10))
        self.assertFalse(is_valid_move(new_board(), 0))

    def test_make_move_places_mark_without_mutating_original(self):
        board = new_board()
        new = make_move(board, 1, "X")
        self.assertEqual(new[0], "X")
        self.assertEqual(board[0], " ")  # original untouched

    def test_parse_position_valid(self):
        self.assertEqual(parse_position("5"), 5)

    def test_parse_position_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            parse_position("10")

    def test_parse_position_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            parse_position("abc")


class TestWinDetection(unittest.TestCase):
    def test_row_win(self):
        board = board_from("XXX......")
        self.assertEqual(check_winner(board), "X")

    def test_column_win(self):
        board = board_from("O..O..O..")
        self.assertEqual(check_winner(board), "O")

    def test_diagonal_win(self):
        board = board_from("X...X...X")
        self.assertEqual(check_winner(board), "X")

    def test_anti_diagonal_win(self):
        board = board_from("..X.X.X..")
        self.assertEqual(check_winner(board), "X")

    def test_no_winner_on_empty_board(self):
        self.assertIsNone(check_winner(new_board()))

    def test_no_winner_without_three_in_a_row(self):
        board = board_from("XO.XO....")
        self.assertIsNone(check_winner(board))


class TestDraw(unittest.TestCase):
    def test_full_board_no_winner_is_draw(self):
        board = board_from("XOXXOOOXX")
        self.assertIsNone(check_winner(board))
        self.assertTrue(is_draw(board))

    def test_full_board_with_winner_is_not_draw(self):
        board = board_from("XXXOO..OX")
        self.assertFalse(is_draw(board))

    def test_non_full_board_is_not_draw(self):
        self.assertFalse(is_draw(new_board()))


class TestComputerMove(unittest.TestCase):
    def test_takes_immediate_win_over_everything_else(self):
        # O has two in a row (positions 1,2 -> indices 0,1), winning move is 3.
        board = board_from("OO.......")
        self.assertEqual(computer_move(board), 3)

    def test_blocks_human_immediate_win(self):
        # X has two in a row (positions 1,2), O must block at 3.
        board = board_from("XX.......")
        self.assertEqual(computer_move(board), 3)

    def test_prefers_win_over_block(self):
        # O can win at position 3 (completing 1,2,3), while X separately
        # threatens to win at position 6 (completing 4,5,6). Win must come first.
        board = board_from("OO.XX....")
        self.assertEqual(computer_move(board), 3)

    def test_takes_center_when_open_and_no_win_or_block(self):
        board = new_board()
        self.assertEqual(computer_move(board), 5)

    def test_takes_a_corner_when_center_taken(self):
        board = board_from("....X....")  # center taken by X, no win/block available
        move = computer_move(board)
        self.assertIn(move, [1, 3, 7, 9])

    def test_always_returns_a_legal_move(self):
        board = board_from("XO.XO....")
        move = computer_move(board)
        self.assertTrue(is_valid_move(board, move))


if __name__ == "__main__":
    unittest.main()
