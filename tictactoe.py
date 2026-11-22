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


def prompt_human_move(board):
    while True:
        text = input("Your move (1-9): ").strip()
        try:
            pos = parse_position(text)
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue
        if not is_valid_move(board, pos):
            print("That square is already taken. Try again.")
            continue
        return pos


def play_one_game():
    board = new_board()
    print(display_board(board))

    while True:
        pos = prompt_human_move(board)
        board = make_move(board, pos, HUMAN)
        print()
        print(display_board(board))

        winner = check_winner(board)
        if winner:
            print(f"\n{winner} wins!")
            return
        if is_draw(board):
            print("\nIt's a draw!")
            return

        comp_pos = computer_move(board)
        board = make_move(board, comp_pos, COMPUTER)
        print(f"\nComputer plays {comp_pos}.")
        print(display_board(board))

        winner = check_winner(board)
        if winner:
            print(f"\n{winner} wins!")
            return
        if is_draw(board):
            print("\nIt's a draw!")
            return


def main():
    while True:
        play_one_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
