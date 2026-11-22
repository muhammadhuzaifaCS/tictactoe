"""Terminal tic-tac-toe vs. a simple computer opponent. See spec.md for the rules."""
import sys

HUMAN = "X"
COMPUTER = "O"

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]

CORNERS = [0, 2, 6, 8]
SIDES = [1, 3, 5, 7]
CENTER = 4


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


def _winning_move_for(board, mark):
    """Return a 1-indexed position that gives `mark` an immediate win, or None."""
    for pos in range(1, 10):
        if is_valid_move(board, pos):
            if check_winner(make_move(board, pos, mark)) == mark:
                return pos
    return None


def computer_move(board):
    """Return the 1-indexed position the computer should play."""
    win = _winning_move_for(board, COMPUTER)
    if win is not None:
        return win

    block = _winning_move_for(board, HUMAN)
    if block is not None:
        return block

    if board[CENTER] == " ":
        return CENTER + 1

    for i in CORNERS:
        if board[i] == " ":
            return i + 1

    for i in SIDES:
        if board[i] == " ":
            return i + 1

    raise ValueError("No move available on a full board")


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


def play_one_game():
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

        comp_pos = computer_move(board)
        board = make_move(board, comp_pos, COMPUTER)
        print(f"\nComputer plays {comp_pos}.")
        print(display_board(board))

        result = announce(board)
        if result:
            return result


def main():
    score = new_score()
    while True:
        result = play_one_game()
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
