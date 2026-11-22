# spec.md — Round 1

Covers R1-R6 from problem.md.

- Board: 9 positions, numbered 1-9 (left-to-right, top-to-bottom), shown as a 3x3 grid.
  Positions already taken show `X` or `O`; empty ones show their number.
- Human is always `X`, moves first. Computer is always `O`.
- Human move: type a number 1-9. Invalid input (not a number, out of range, or an
  already-taken position) prints a message and asks again — never crashes.
- Computer move: picks, in order of priority: (1) a move that wins immediately, (2) a
  move that blocks the human's immediate win, (3) the center (5) if open, (4) any open
  corner (1,3,7,9), (5) any open side (2,4,6,8).
- After each move (human or computer), the board is reprinted.
- Win: three of the same mark in a row, column, or diagonal — announce the winner by
  mark (`X` or `O`) and stop.
- Draw: board full, no winner — announce a draw and stop.
- After a game ends: ask "Play again? (y/n)". `y` starts a new game (fresh board); `n`
  exits. (Round 2 changes this: other answers no longer exit; see below.)


## Round 2

Covers R7-R9 from problem.md. Everything in Round 1 still applies except where noted.

- Session: one run of the program. The score exists only in memory and starts at
  0 wins, 0 losses, 0 draws; it is not saved between runs.
- Score is from the human player's point of view (R7): a win is a game where `X` wins, a
  loss is a game where `O` (the computer) wins, a draw is a full board with no winner.
  Each finished game adds exactly one to exactly one of the three counts.
- Score display format (R8, R9), one line: `Score - Wins: 2  Losses: 1  Draws: 0`.
- After each finished game, print the updated score, then ask "Play again? (y/n)" (R8).
- Play-again prompt (R9, changes Round 1): input is trimmed and case-insensitive. `y`
  starts a new game, `n` quits. Any other answer prints a message and asks again.
- Quitting mid-game (new, decided with the user): typing `q` (any case) at the move
  prompt ends the session immediately. The unfinished game counts as a loss for the
  player. The move prompt reads "Your move (1-9, or q to quit): ".
- When the session ends, by `n` or by `q`, print the final score (R9) as
  `Final score - Wins: 2  Losses: 1  Draws: 0` and exit. Quitting mid-game prints the
  final score with the loss already included.
- End of input (Ctrl-D / Ctrl-Z, `EOFError`) is treated as quitting at either prompt, so
  the program never crashes or loops forever when input runs out.


## Round 3

Covers R10-R12 from problem.md. Everything in Rounds 1 and 2 still applies except where noted.

- Undo command (R10): at the move prompt, `undo` or `u` (trimmed, any case) takes back the
  player's most recent move instead of placing a mark. Decided with the user.
- Undo removes the pair (R11): the player's last move and the computer's reply to it are both
  removed, so the board is exactly as it was just before the player's last move, and it is the
  player's turn again. The restored board is printed.
- Unlimited undo (decided with the user): each undo steps back one more player+computer pair,
  until the board is empty.
- Nothing to undo (R12): if no player move has been made in the current game (including after
  undoing back to the start), print "Nothing to undo." and ask for a square again. The board
  is not changed.
- History is per game: a new game starts with no history, so undo never reaches into a
  previous game.
- Score is never changed by an undo (R12). A game only counts when it ends, and an undone
  move cannot end a game, because an undo is only offered while the game is still running.
- Changes earlier behavior: the move prompt now reads
  "Your move (1-9, u to undo, or q to quit): " (was "Your move (1-9, or q to quit): ").
  The invalid-input message now reads "Please enter a number from 1 to 9, u to undo, or q to quit."
- Implementation note: history is a list of boards, one snapshot taken before each player
  move; `undo_move(history)` returns `(board, history)` without the last snapshot, or `None`.
