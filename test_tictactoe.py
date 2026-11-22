import json
import os
import tempfile
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
    EASY,
    HARD,
    EASY_RANDOM_CHANCE,
    parse_difficulty,
    choose_computer_move,
    load_score,
    save_score,
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


def play_all_human_lines(board, outcomes):
    """Try every possible human move; the computer answers with computer_move.

    Appends 'win' / 'loss' / 'draw' (human's point of view) to `outcomes` for every
    finished game. Human is X and moves first, as in the real game.
    """
    for pos in range(1, 10):
        if not is_valid_move(board, pos):
            continue
        after_human = make_move(board, pos, "X")
        result = game_result(after_human)
        if result is not None:
            outcomes.append(result)
            continue
        reply = computer_move(after_human)
        assert is_valid_move(after_human, reply), f"illegal reply {reply} on {after_human}"
        after_computer = make_move(after_human, reply, "O")
        result = game_result(after_computer)
        if result is not None:
            outcomes.append(result)
            continue
        play_all_human_lines(after_computer, outcomes)


class TestComputerMove(unittest.TestCase):
    def test_R3_takes_immediate_win_over_everything_else(self):
        # O has two in a row (positions 1,2 -> indices 0,1), winning move is 3.
        board = board_from("OO.......")
        self.assertEqual(computer_move(board), 3)

    def test_R3_blocks_human_immediate_win(self):
        # X has two in a row (positions 1,2), O must block at 3.
        board = board_from("XX.......")
        self.assertEqual(computer_move(board), 3)

    def test_R3_prefers_win_over_block(self):
        # O can win at position 3 (completing 1,2,3), while X separately
        # threatens to win at position 6 (completing 4,5,6). Win must come first.
        board = board_from("OO.XX....")
        self.assertEqual(computer_move(board), 3)

    def test_R3_takes_a_corner_when_center_taken(self):
        board = board_from("....X....")  # X in the center: a side reply loses, a corner draws
        move = computer_move(board)
        self.assertIn(move, [1, 3, 7, 9])

    def test_R3_always_returns_a_legal_move(self):
        board = board_from("XO.XO....")
        move = computer_move(board)
        self.assertTrue(is_valid_move(board, move))

    def test_R3_legal_move_on_empty_board(self):
        board = new_board()
        self.assertTrue(is_valid_move(board, computer_move(board)))

    def test_R3_does_not_mutate_the_board(self):
        board = board_from("X...O...X")
        before = list(board)
        computer_move(board)
        self.assertEqual(board, before)

    def test_R3_full_board_has_no_move(self):
        board = board_from("XOXXOOOXX")
        with self.assertRaises(ValueError):
            computer_move(board)

    def test_R3_answers_a_corner_opening_with_the_center(self):
        # After X takes a corner, the center is the only reply that does not lose.
        for corner in "X........", "..X......", "......X..", "........X":
            with self.subTest(board=corner):
                self.assertEqual(computer_move(board_from(corner)), 5)

    def test_R3_defends_against_the_opposite_corners_trap(self):
        # X has opposite corners 1 and 9, O has the center. A corner reply (3) lets X fork
        # and win; the computer must take a side instead.
        board = board_from("X...O...X")
        self.assertIn(computer_move(board), [2, 4, 6, 8])

    def test_R3_avoids_a_losing_move_when_a_fork_is_coming(self):
        # X has 1 and 8, O has the center, O to move. Whatever square the computer
        # picks, X must not be able to force a win from there.
        board = board_from("X...O..X.")
        outcomes = []
        reply = computer_move(board)
        after = make_move(board, reply, "O")
        if game_result(after) is None:
            play_all_human_lines(after, outcomes)
        self.assertNotIn("win", outcomes)

    def test_R3_computer_never_loses_against_any_human_play(self):
        # Exhaustive: every human move at every turn, computer answers each time.
        outcomes = []
        play_all_human_lines(new_board(), outcomes)
        self.assertGreater(len(outcomes), 0)
        self.assertNotIn("win", outcomes)

    def test_R3_human_can_still_draw_and_computer_can_still_win(self):
        # The opponent is unbeatable, not unplayable: good play draws, mistakes lose.
        outcomes = []
        play_all_human_lines(new_board(), outcomes)
        self.assertIn("draw", outcomes)
        self.assertIn("loss", outcomes)

    def test_R3_same_board_gets_the_same_reply(self):
        board = board_from("X...O...X")
        self.assertEqual(computer_move(board), computer_move(list(board)))

    def test_R3_wins_as_soon_as_it_can_rather_than_later(self):
        # O can win right now at 6, or set up a slower win elsewhere. It must take 6.
        board = board_from("XX.OO.X..")
        self.assertEqual(computer_move(board), 6)


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
        self.assertTrue(is_undo_command("  UNDO \n"))
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


class FixedRng:
    """Stand-in for random.Random: random() returns `roll`; choice() returns the item at `pick`."""

    def __init__(self, roll, pick=0):
        self.roll = roll
        self.pick = pick
        self.rolls = 0
        self.choices = []

    def random(self):
        self.rolls += 1
        return self.roll

    def choice(self, seq):
        self.choices.append(list(seq))
        return seq[self.pick]


def legal_squares(board):
    return [p for p in range(1, 10) if is_valid_move(board, p)]


class TestParseDifficulty(unittest.TestCase):
    def test_R13_easy_and_hard_words(self):
        self.assertEqual(parse_difficulty("easy"), EASY)
        self.assertEqual(parse_difficulty("hard"), HARD)

    def test_R13_one_letter_forms(self):
        self.assertEqual(parse_difficulty("e"), EASY)
        self.assertEqual(parse_difficulty("h"), HARD)

    def test_R13_case_and_whitespace_ignored(self):
        self.assertEqual(parse_difficulty("  EaSy \n"), EASY)
        self.assertEqual(parse_difficulty("\tHARD "), HARD)

    def test_R13_anything_else_is_invalid(self):
        for text in ["", "  ", "medium", "1", "2", "y", "easyy", "ha rd", "q"]:
            self.assertIsNone(parse_difficulty(text), text)


class TestHardDifficulty(unittest.TestCase):
    def test_R14_hard_matches_optimal_play_on_every_board_reachable_early(self):
        boards = [
            "X........", "....X....", "X...O...X", "XX.......", "X.O.X....",
            "XX.O.....", "X.......O",
        ]
        for s in boards:
            board = board_from(s)
            self.assertEqual(
                choose_computer_move(board, HARD, FixedRng(0.0)), computer_move(board), s
            )

    def test_R14_hard_never_rolls_the_dice(self):
        rng = FixedRng(0.0)
        choose_computer_move(board_from("X........"), HARD, rng)
        self.assertEqual(rng.rolls, 0)
        self.assertEqual(rng.choices, [])

    def test_R14_hard_still_takes_win_and_blocks(self):
        rng = FixedRng(0.0)
        self.assertEqual(choose_computer_move(board_from("OO.XX...."), HARD, rng), 3)
        self.assertEqual(choose_computer_move(board_from("XX..O...."), HARD, rng), 3)


class TestEasyDifficulty(unittest.TestCase):
    def test_R15_low_roll_plays_a_random_legal_move_from_the_legal_squares(self):
        board = board_from("XX..O....")  # optimal is 3 (block); legal are 3,4,6,7,8,9
        rng = FixedRng(0.0, pick=4)
        move = choose_computer_move(board, EASY, rng)
        self.assertEqual(rng.choices, [[3, 4, 6, 7, 8, 9]])
        self.assertEqual(move, 8)

    def test_R15_high_roll_plays_the_optimal_move(self):
        board = board_from("XX..O....")
        rng = FixedRng(0.99)
        self.assertEqual(choose_computer_move(board, EASY, rng), computer_move(board))
        self.assertEqual(rng.choices, [])

    def test_R15_the_chance_is_one_in_three(self):
        self.assertAlmostEqual(EASY_RANDOM_CHANCE, 1 / 3)

    def test_R15_roll_just_under_one_third_is_random_just_over_is_optimal(self):
        board = board_from("XX..O....")
        under = FixedRng(EASY_RANDOM_CHANCE - 0.001, pick=5)  # picks 9
        over = FixedRng(EASY_RANDOM_CHANCE + 0.001, pick=5)
        self.assertEqual(choose_computer_move(board, EASY, under), 9)
        self.assertEqual(choose_computer_move(board, EASY, over), 3)

    def test_R15_dice_are_rolled_on_every_turn(self):
        rng = FixedRng(0.99)
        for _ in range(4):
            choose_computer_move(board_from("X........"), EASY, rng)
        self.assertEqual(rng.rolls, 4)

    def test_R15_easy_always_returns_a_legal_move(self):
        import random

        rng = random.Random(7)
        for s in ["X........", "XX..O....", "XOXOX.O..", "XOXXOOOX."]:
            board = board_from(s)
            for _ in range(200):
                self.assertIn(choose_computer_move(board, EASY, rng), legal_squares(board))

    def test_R15_about_one_in_three_turns_deviate_from_optimal(self):
        import random

        board = board_from("XX..O....")  # 6 legal squares, only 3 is optimal
        rng = random.Random(1)
        trials = 6000
        deviations = sum(
            choose_computer_move(board, EASY, rng) != computer_move(board) for _ in range(trials)
        )
        expected = EASY_RANDOM_CHANCE * 5 / 6  # random move is the optimal one 1 time in 6
        self.assertAlmostEqual(deviations / trials, expected, delta=0.03)

    def test_R15_the_player_can_win_on_easy(self):
        # The computer always rolls "random" and picks the lowest legal square (a bad move).
        rng = FixedRng(0.0, pick=0)
        board = new_board()
        for human_pos in [5, 3, 7]:
            self.assertTrue(is_valid_move(board, human_pos))
            board = make_move(board, human_pos, "X")
            if check_winner(board):
                break
            board = make_move(board, choose_computer_move(board, EASY, rng), "O")
        self.assertEqual(check_winner(board), "X")

    def test_R15_easy_does_not_mutate_the_board(self):
        board = board_from("X...O....")
        before = list(board)
        choose_computer_move(board, EASY, FixedRng(0.0))
        self.assertEqual(board, before)

    def test_R15_unknown_difficulty_is_rejected(self):
        with self.assertRaises(ValueError):
            choose_computer_move(new_board(), "medium", FixedRng(0.0))


class ScoreFileTestCase(unittest.TestCase):
    """Gives each test a private temporary folder; the real score.json is never touched."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = os.path.join(self._tmp.name, "score.json")

    def write_text(self, text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def read_json(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)


class TestSaveScore(ScoreFileTestCase):
    def test_R16_save_writes_wins_losses_draws_to_the_file(self):
        score = {"wins": 2, "losses": 1, "draws": 3}
        self.assertTrue(save_score(score, self.path))
        self.assertEqual(self.read_json(), {"wins": 2, "losses": 1, "draws": 3})

    def test_R16_save_replaces_the_previous_contents(self):
        save_score({"wins": 5, "losses": 5, "draws": 5}, self.path)
        save_score({"wins": 0, "losses": 1, "draws": 0}, self.path)
        self.assertEqual(self.read_json(), {"wins": 0, "losses": 1, "draws": 0})

    def test_R16_save_overwrites_an_invalid_file(self):
        self.write_text("garbage")
        self.assertTrue(save_score({"wins": 1, "losses": 0, "draws": 0}, self.path))
        self.assertEqual(self.read_json(), {"wins": 1, "losses": 0, "draws": 0})

    def test_R16_save_does_not_change_the_score(self):
        score = {"wins": 1, "losses": 2, "draws": 3}
        save_score(score, self.path)
        self.assertEqual(score, {"wins": 1, "losses": 2, "draws": 3})

    def test_R16_each_finished_game_result_can_be_saved(self):
        score = new_score()
        for result in ("win", "loss", "draw", "loss"):
            score = record_result(score, result)
            save_score(score, self.path)
            self.assertEqual(self.read_json(), score)
        self.assertEqual(self.read_json(), {"wins": 1, "losses": 2, "draws": 1})

    def test_R16_save_to_an_unwritable_path_returns_false_and_does_not_raise(self):
        bad = os.path.join(self._tmp.name, "no-such-folder", "score.json")
        self.assertFalse(save_score({"wins": 1, "losses": 0, "draws": 0}, bad))
        self.assertFalse(os.path.exists(bad))


class TestLoadScore(ScoreFileTestCase):
    def test_R17_load_returns_the_saved_wins_losses_draws(self):
        self.write_text('{"wins": 4, "losses": 2, "draws": 7}')
        self.assertEqual(load_score(self.path), {"wins": 4, "losses": 2, "draws": 7})

    def test_R17_load_accepts_zero_counts(self):
        self.write_text('{"wins": 0, "losses": 0, "draws": 0}')
        self.assertEqual(load_score(self.path), {"wins": 0, "losses": 0, "draws": 0})

    def test_R17_key_order_and_whitespace_in_the_file_do_not_matter(self):
        self.write_text('\n{ "draws": 3,\n  "wins": 1,\n  "losses": 2 }\n')
        self.assertEqual(load_score(self.path), {"wins": 1, "losses": 2, "draws": 3})

    def test_R17_save_then_load_round_trips(self):
        score = {"wins": 9, "losses": 8, "draws": 7}
        save_score(score, self.path)
        self.assertEqual(load_score(self.path), score)

    def test_R17_counting_continues_from_the_loaded_score(self):
        save_score({"wins": 2, "losses": 5, "draws": 1}, self.path)
        score = record_result(load_score(self.path), "draw")
        self.assertEqual(score, {"wins": 2, "losses": 5, "draws": 2})
        self.assertEqual(format_score(score), "Score - Wins: 2  Losses: 5  Draws: 2")

    def test_R17_loaded_score_is_shown_in_the_final_score(self):
        save_score({"wins": 3, "losses": 1, "draws": 0}, self.path)
        self.assertEqual(
            format_final_score(load_score(self.path)),
            "Final score - Wins: 3  Losses: 1  Draws: 0",
        )

    def test_R17_two_runs_in_a_row_accumulate(self):
        # First run: one win saved. Second run: loads it, adds a loss.
        save_score(record_result(load_score(self.path), "win"), self.path)
        save_score(record_result(load_score(self.path), "loss"), self.path)
        self.assertEqual(self.read_json(), {"wins": 1, "losses": 1, "draws": 0})


class TestLoadScoreMissingOrInvalid(ScoreFileTestCase):
    def assert_starts_at_zero(self):
        self.assertEqual(load_score(self.path), {"wins": 0, "losses": 0, "draws": 0})

    def test_R18_missing_file_starts_at_zero(self):
        self.assertFalse(os.path.exists(self.path))
        self.assert_starts_at_zero()

    def test_R18_missing_file_is_not_created_by_loading(self):
        load_score(self.path)
        self.assertFalse(os.path.exists(self.path))

    def test_R18_empty_file_starts_at_zero(self):
        self.write_text("")
        self.assert_starts_at_zero()

    def test_R18_malformed_json_starts_at_zero(self):
        self.write_text('{"wins": 1, "losses": ')
        self.assert_starts_at_zero()

    def test_R18_not_json_at_all_starts_at_zero(self):
        self.write_text("hello world")
        self.assert_starts_at_zero()

    def test_R18_json_that_is_not_an_object_starts_at_zero(self):
        for text in ("[1, 2, 3]", "5", '"wins"', "null", "true"):
            with self.subTest(text=text):
                self.write_text(text)
                self.assert_starts_at_zero()

    def test_R18_missing_key_starts_at_zero(self):
        self.write_text('{"wins": 1, "losses": 2}')
        self.assert_starts_at_zero()

    def test_R18_extra_key_starts_at_zero(self):
        self.write_text('{"wins": 1, "losses": 2, "draws": 3, "extra": 4}')
        self.assert_starts_at_zero()

    def test_R18_negative_count_starts_at_zero(self):
        self.write_text('{"wins": -1, "losses": 2, "draws": 3}')
        self.assert_starts_at_zero()

    def test_R18_non_integer_counts_start_at_zero(self):
        for bad in ("1.5", "2.0", '"3"', "null", "true", "false", "[1]", "{}"):
            with self.subTest(wins=bad):
                self.write_text('{"wins": %s, "losses": 0, "draws": 0}' % bad)
                self.assert_starts_at_zero()

    def test_R18_one_bad_field_rejects_the_whole_file(self):
        # wins and losses are fine; draws is bad. Nothing is partly loaded.
        self.write_text('{"wins": 5, "losses": 5, "draws": "many"}')
        self.assert_starts_at_zero()

    def test_R18_unreadable_file_starts_at_zero(self):
        # A folder where the file should be cannot be read as a file.
        os.mkdir(self.path)
        self.assert_starts_at_zero()

    def test_R18_file_that_is_not_text_starts_at_zero(self):
        with open(self.path, "wb") as f:
            f.write(b"\xff\xfe\x00\x80\x81")
        self.assert_starts_at_zero()

    def test_R18_invalid_file_is_left_alone_by_loading(self):
        self.write_text("garbage")
        load_score(self.path)
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(f.read(), "garbage")

    def test_R18_each_call_returns_a_fresh_score(self):
        first = load_score(self.path)
        first["wins"] = 99
        self.assert_starts_at_zero()


if __name__ == "__main__":
    unittest.main()
