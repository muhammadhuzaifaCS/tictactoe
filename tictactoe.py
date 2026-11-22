"""Terminal tic-tac-toe vs. the computer (Easy or Hard). See spec.md for the rules."""
import random
import sys
from functools import lru_cache

HUMAN = "X"
COMPUTER = "O"

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def new_board():
    return [" "] * 9


def display_board(board):
    def cell(i):
        return board[i] if board[i] != " " else str(i + 1)

    rows = []
    for r in range(3):
        rows.append(" | ".join(cell(r * 3 + c) for c in range(3)))
    return "\n---------\n".join(rows)


def is_valid_move(board, pos):
    """pos is 1-9 (1-indexed, as shown to the player)."""
    return isinstance(pos, int) and 1 <= pos <= 9 and board[pos - 1] == " "


def make_move(board, pos, mark):
    """Return a new board with mark placed at 1-indexed pos."""
    new = list(board)
    new[pos - 1] = mark
    return new


def check_winner(board):
    """Return 'X', 'O', or None."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return " " not in board


def is_draw(board):
    return is_full(board) and check_winner(board) is None


@lru_cache(maxsize=None)
def _minimax(board, mark_to_move, depth):
    """Value of `board` (a tuple, so results can be cached) for the computer with `mark_to_move` about to play.

    Positive = computer wins, 0 = draw, negative = computer loses. Wins found sooner
    score higher and losses found later score higher (the value is offset by `depth`).
    """
    winner = check_winner(board)
    if winner == COMPUTER:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if is_full(board):
        return 0

    other = HUMAN if mark_to_move == COMPUTER else COMPUTER
    values = [
        _minimax(tuple(make_move(board, pos, mark_to_move)), other, depth + 1)
        for pos in range(1, 10)
        if is_valid_move(board, pos)
    ]
    return max(values) if mark_to_move == COMPUTER else min(values)


def computer_move(board):
    """Return the 1-indexed position the computer (O) should play: optimal, never loses.

    Ties go to the lowest-numbered square, so the same board always gets the same reply.
    """
    best_pos = None
    best_value = None
    for pos in range(1, 10):
        if not is_valid_move(board, pos):
            continue
        value = _minimax(tuple(make_move(board, pos, COMPUTER)), HUMAN, 1)
        if best_value is None or value > best_value:
            best_pos, best_value = pos, value

    if best_pos is None:
        raise ValueError("No move available on a full board")
    return best_pos


def parse_position(text):
    """Parse a 1-9 position from input text. Raises ValueError if invalid."""
    pos = int(text)
    if not (1 <= pos <= 9):
        raise ValueError(f"Position must be 1-9, got {pos}")
    return pos


# --- Round 2: session score (R7-R9) -------------------------------------------

QUIT = "quit"


def new_score():
    return {"wins": 0, "losses": 0, "draws": 0}


def game_result(board):
    """Result from the human's point of view: 'win', 'loss', 'draw', or None if unfinished."""
    winner = check_winner(board)
    if winner == HUMAN:
        return "win"
    if winner == COMPUTER:
        return "loss"
    if is_full(board):
        return "draw"
    return None


_RESULT_KEYS = {"win": "wins", "loss": "losses", "draw": "draws"}


def record_result(score, result):
    """Return a new score with one game's result added. Does not mutate `score`."""
    if result not in _RESULT_KEYS:
        raise ValueError(f"Unknown result: {result!r}")
    new = dict(score)
    new[_RESULT_KEYS[result]] += 1
    return new


def _score_text(score):
    return f"Wins: {score['wins']}  Losses: {score['losses']}  Draws: {score['draws']}"


def format_score(score):
    return f"Score - {_score_text(score)}"


def format_final_score(score):
    return f"Final score - {_score_text(score)}"


def parse_yes_no(text):
    """True for 'y', False for 'n' (trimmed, any case); None for anything else."""
    answer = text.strip().lower()
    if answer == "y":
        return True
    if answer == "n":
        return False
    return None


def is_quit_command(text):
    return text.strip().lower() == "q"


# --- Round 3: undo (R10-R12) --------------------------------------------------

UNDO = "undo"


def is_undo_command(text):
    """True for 'undo' or 'u' (trimmed, any case)."""
    return text.strip().lower() in ("undo", "u")


def undo_move(history):
    """Undo the player's last move and the computer's reply to it.

    `history` is a list of boards, one snapshot taken just before each player move.
    Returns (board, new_history), where board is the snapshot to go back to, or None
    if there is nothing to undo. Does not mutate `history`.
    """
    if not history:
        return None
    return list(history[-1]), history[:-1]


# --- Round 5: difficulty (R13-R15) --------------------------------------------

EASY = "easy"
HARD = "hard"
EASY_RANDOM_CHANCE = 1 / 3


def parse_difficulty(text):
    """EASY for 'easy'/'e', HARD for 'hard'/'h' (trimmed, any case); None for anything else."""
    answer = text.strip().lower()
    if answer in ("easy", "e"):
        return EASY
    if answer in ("hard", "h"):
        return HARD
    return None


def choose_computer_move(board, difficulty, rng):
    """Return the 1-indexed position the computer plays on the given difficulty.

    HARD: always `computer_move(board)` (optimal). EASY: with probability
    EASY_RANDOM_CHANCE a random legal move, otherwise the optimal move.
    `rng` needs `random()` and `choice()` (a `random.Random` works); it is passed in
    so tests can control the dice.
    """
    if difficulty == HARD:
        return computer_move(board)
    if difficulty != EASY:
        raise ValueError(f"Unknown difficulty: {difficulty!r}")
    if rng.random() < EASY_RANDOM_CHANCE:
        legal = [pos for pos in range(1, 10) if is_valid_move(board, pos)]
        if not legal:
            raise ValueError("No move available on a full board")
        return rng.choice(legal)
    return computer_move(board)


# --- Input/print loop (not unit-tested; logic lives in the functions above) ---


def read_line(prompt):
    """input() that returns None at end of input instead of raising EOFError."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return None


def prompt_human_move(board):
    """Return a 1-9 position, UNDO, or QUIT if the player quits (or input ends)."""
    while True:
        text = read_line("Your move (1-9, u to undo, or q to quit): ")
        if text is None or is_quit_command(text):
            return QUIT
        if is_undo_command(text):
            return UNDO
        try:
            pos = parse_position(text.strip())
        except ValueError:
            print("Please enter a number from 1 to 9, u to undo, or q to quit.")
            continue
        if not is_valid_move(board, pos):
            print("That square is already taken. Try again.")
            continue
        return pos


def prompt_difficulty():
    """Return EASY or HARD, or None if input ends. Asks again on any other answer."""
    while True:
        text = read_line("Choose difficulty (easy/hard): ")
        if text is None:
            return None
        difficulty = parse_difficulty(text)
        if difficulty is not None:
            return difficulty
        print("Please answer easy or hard.")


def prompt_play_again():
    """Return True to play again, False to quit (also False if input ends)."""
    while True:
        text = read_line("\nPlay again? (y/n): ")
        if text is None:
            return False
        answer = parse_yes_no(text)
        if answer is not None:
            return answer
        print("Please answer y or n.")


def announce(board):
    result = game_result(board)
    if result == "draw":
        print("\nIt's a draw!")
    elif result is not None:
        print(f"\n{check_winner(board)} wins!")
    return result


def play_one_game(difficulty=HARD, rng=random):
    """Play one game. Return 'win', 'loss', 'draw', or QUIT (player quit mid-game)."""
    board = new_board()
    history = []  # boards from just before each player move (for undo)
    print(display_board(board))

    while True:
        pos = prompt_human_move(board)
        if pos == QUIT:
            return QUIT
        if pos == UNDO:
            undone = undo_move(history)
            if undone is None:
                print("Nothing to undo.")
            else:
                board, history = undone
                print("\nUndid your last move and the computer's reply.")
                print(display_board(board))
            continue
        history = history + [board]
        board = make_move(board, pos, HUMAN)
        print()
        print(display_board(board))

        result = announce(board)
        if result:
            return result

        comp_pos = choose_computer_move(board, difficulty, rng)
        board = make_move(board, comp_pos, COMPUTER)
        print(f"\nComputer plays {comp_pos}.")
        print(display_board(board))

        result = announce(board)
        if result:
            return result


def main():
    score = new_score()
    difficulty = prompt_difficulty()  # asked once; stays for the whole session (R13)
    while difficulty is not None:
        result = play_one_game(difficulty)
        if result == QUIT:
            print("\nYou quit mid-game; that counts as a loss.")
            score = record_result(score, "loss")
            break
        score = record_result(score, result)
        print(format_score(score))
        if not prompt_play_again():
            break
    print(format_final_score(score))
    return 0


if __name__ == "__main__":
    sys.exit(main())
