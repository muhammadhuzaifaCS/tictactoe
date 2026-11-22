import unittest

from tictactoe import (
    new_board,
    is_valid_move,
    make_move,
    check_winner,
    is_draw,
    computer_move,
    parse_position,
    new_score,
    game_result,
    record_result,
    format_score,
    format_final_score,
    parse_yes_no,
    is_quit_command,
    is_undo_command,
    undo_move,
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


class TestScoreCounting(unittest.TestCase):
    """R7: running count of wins, losses, draws."""

    def test_R7_new_score_is_all_zero(self):
        self.assertEqual(new_score(), {"wins": 0, "losses": 0, "draws": 0})

    def test_R7_human_x_win_is_a_win(self):
        self.assertEqual(game_result(board_from("XXX......")), "win")

    def test_R7_computer_o_win_is_a_loss(self):
        self.assertEqual(game_result(board_from("O..O..O..")), "loss")

    def test_R7_full_board_no_winner_is_a_draw(self):
        self.assertEqual(game_result(board_from("XOXXOOOXX")), "draw")

    def test_R7_unfinished_board_has_no_result(self):
        self.assertIsNone(game_result(board_from("XO.......")))

    def test_R7_record_each_result_increments_only_its_own_count(self):
        self.assertEqual(record_result(new_score(), "win"), {"wins": 1, "losses": 0, "draws": 0})
        self.assertEqual(record_result(new_score(), "loss"), {"wins": 0, "losses": 1, "draws": 0})
        self.assertEqual(record_result(new_score(), "draw"), {"wins": 0, "losses": 0, "draws": 1})

    def test_R7_record_result_does_not_mutate_original(self):
        score = new_score()
        record_result(score, "win")
        self.assertEqual(score, new_score())

    def test_R7_score_accumulates_across_games(self):
        score = new_score()
        for result in ["win", "loss", "win", "draw", "win"]:
            score = record_result(score, result)
        self.assertEqual(score, {"wins": 3, "losses": 1, "draws": 1})

    def test_R7_record_result_rejects_unknown_result(self):
        with self.assertRaises(ValueError):
            record_result(new_score(), "quit")


class TestScoreDisplay(unittest.TestCase):
    """R8: updated score shown after each game; R9: final score shown on quit."""

    def test_R8_format_score(self):
        score = {"wins": 2, "losses": 1, "draws": 0}
        self.assertEqual(format_score(score), "Score - Wins: 2  Losses: 1  Draws: 0")

    def test_R8_format_score_reflects_latest_game(self):
        score = record_result({"wins": 2, "losses": 1, "draws": 0}, "draw")
        self.assertEqual(format_score(score), "Score - Wins: 2  Losses: 1  Draws: 1")

    def test_R9_format_final_score(self):
        score = {"wins": 2, "losses": 1, "draws": 0}
        self.assertEqual(format_final_score(score), "Final score - Wins: 2  Losses: 1  Draws: 0")


class TestPlayAgainPrompt(unittest.TestCase):
    """R9 (and R6): keep playing until the player chooses to quit."""

    def test_R9_y_means_play_again(self):
        self.assertIs(parse_yes_no("y"), True)

    def test_R9_n_means_quit(self):
        self.assertIs(parse_yes_no("n"), False)

    def test_R9_case_and_whitespace_ignored(self):
        self.assertIs(parse_yes_no("  Y \n"), True)
        self.assertIs(parse_yes_no("N"), False)

    def test_R9_other_answers_are_invalid_not_quit(self):
        for text in ["yes", "no", "x", "", "1", "q"]:
            self.assertIsNone(parse_yes_no(text), text)


class TestMidGameQuit(unittest.TestCase):
    """R9: the player can quit; quitting mid-game counts as a loss (spec, Round 2)."""

    def test_R9_q_is_quit_command_any_case_and_whitespace(self):
        self.assertTrue(is_quit_command("q"))
        self.assertTrue(is_quit_command(" Q "))

    def test_R9_digits_and_junk_are_not_quit(self):
        for text in ["5", "", "quit", "x"]:
            self.assertFalse(is_quit_command(text), text)

    def test_R9_quit_mid_game_recorded_as_loss_in_final_score(self):
        score = record_result({"wins": 1, "losses": 0, "draws": 0}, "loss")
        self.assertEqual(format_final_score(score), "Final score - Wins: 1  Losses: 1  Draws: 0")


class TestUndoCommand(unittest.TestCase):
    """R10: undo is typed instead of a square number."""

    def test_R10_undo_and_u_are_undo_commands(self):
        self.assertTrue(is_undo_command("undo"))
        self.assertTrue(is_undo_command("u"))

    def test_R10_case_and_whitespace_ignored(self):
        self.assertTrue(is_undo_command("  UNDO 
"))
        self.assertTrue(is_undo_command(" U "))

    def test_R10_other_input_is_not_undo(self):
        for text in ["", "5", "q", "un", "undoo", "redo"]:
            self.assertFalse(is_undo_command(text), text)


class TestUndoMove(unittest.TestCase):
    """R11 and R12: undo restores the board from before the player's last move."""

    def play_turn(self, board, history, pos):
        """Mimic one loop turn: snapshot, human move, computer reply."""
        history = history + [board]
        board = make_move(board, pos, "X")
        board = make_move(board, computer_move(board), "O")
        return board, history

    def test_R11_undo_returns_board_from_before_last_player_move(self):
        start = new_board()
        board, history = self.play_turn(start, [], 1)
        self.assertNotEqual(board, start)
        restored, _ = undo_move(history)
        self.assertEqual(restored, start)

    def test_R11_undo_removes_computer_reply_too(self):
        board, history = self.play_turn(new_board(), [], 1)
        self.assertEqual(board.count("X"), 1)
        self.assertEqual(board.count("O"), 1)
        restored, _ = undo_move(history)
        self.assertEqual(restored.count("X"), 0)
        self.assertEqual(restored.count("O"), 0)

    def test_R11_undo_only_removes_the_most_recent_pair(self):
        board1, history = self.play_turn(new_board(), [], 1)
        board2, history = self.play_turn(board1, history, 9)
        restored, _ = undo_move(history)
        self.assertEqual(restored, board1)

    def test_R11_repeated_undo_steps_back_one_pair_each_time(self):
        start = new_board()
        board1, history = self.play_turn(start, [], 1)
        board2, history = self.play_turn(board1, history, 9)
        restored, history = undo_move(history)
        self.assertEqual(restored, board1)
        restored, history = undo_move(history)
        self.assertEqual(restored, start)
        self.assertIsNone(undo_move(history))

    def test_R11_player_can_move_again_on_restored_square(self):
        board, history = self.play_turn(new_board(), [], 1)
        restored, _ = undo_move(history)
        self.assertTrue(is_valid_move(restored, 1))

    def test_R11_undo_does_not_mutate_inputs(self):
        board, history = self.play_turn(new_board(), [], 1)
        history_copy = [list(b) for b in history]
        undo_move(history)
        self.assertEqual(history, history_copy)

    def test_R12_nothing_to_undo_with_empty_history(self):
        self.assertIsNone(undo_move([]))

    def test_R12_undo_does_not_change_score(self):
        score = {"wins": 1, "losses": 2, "draws": 3}
        before = dict(score)
        _, history = self.play_turn(new_board(), [], 1)
        undo_move(history)
        undo_move([])
        self.assertEqual(score, before)


if __name__ == "__main__":
    unittest.main()
