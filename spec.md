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


## Round 4

Covers the change to R3 in problem.md. Everything in Rounds 1-3 still applies except where noted.

- R3 (changed): the computer plays optimally and never loses. Against any sequence of human
  moves the game ends in a computer win or a draw, never a human win. It still moves
  automatically and always picks a legal move.
- "Optimal" means minimax over the full game tree (the computer is `O`, the human is `X`).
  A position's value is +1 if the computer can force a win, 0 if best play is a draw, -1 if
  the computer would lose.
- Choosing among moves of equal value (new, decided without asking):
  - A win is preferred sooner over later, and a loss (when forced) later over sooner. So the
    computer takes an immediate win when there is one, and otherwise blocks or delays.
  - If several moves are still equal, the lowest-numbered square wins, so the computer is
    deterministic: the same board always gets the same reply.
- Changes earlier behavior: Round 1's priority list (win, block, center, corner, side) no
  longer describes the computer. Winning and blocking an immediate threat still happen, but as
  a result of minimax. The computer no longer always takes the center first.
- Effects on earlier requirements (from problem.md): R4, R5, R7, R8, R11 are unchanged. The
  player can now only draw or lose, so the score will show draws and losses.
- Undo (R10-R12) is unchanged. Because the computer is deterministic, redoing a move after an
  undo gets the same reply.


## Round 5

Covers R13-R15 from problem.md. Everything in Rounds 1-4 still applies except where noted.

- Difficulty prompt (R13): once per session, before the first game, the program asks
  "Choose difficulty (easy/hard): ". Input is trimmed and case-insensitive; `easy` or `e` means
  Easy, `hard` or `h` means Hard. Any other answer prints "Please answer easy or hard." and asks
  again. The choice is never asked again and stays the same for every game in the session
  (playing again does not re-prompt). Accepting the one-letter forms is a decision made without
  asking, in line with `y`/`n`.
- End of input at the difficulty prompt quits cleanly (same rule as the other prompts): no game
  is played and the final score (all zeros) is printed.
- Hard (R14): exactly the Round 4 computer: optimal minimax, deterministic, never loses.
- Easy (R15): each time the computer takes a turn, it plays a uniformly random legal move with
  probability 1/3 ("about one in three"); otherwise it plays the optimal move exactly as on Hard.
  The random chance is rolled fresh on every computer turn. A random move may happen to equal
  the optimal one. Because of this the player can win on Easy.
- Changes earlier behavior:
  - R3 now describes the computer on Hard only (its wording is unchanged). On Easy, R15 applies.
  - Round 4's note "the same board always gets the same reply" is true on Hard only. On Easy it
    can differ, so after an undo (R11) the computer's reply to a redone move may be different.
  - Round 4's "the player can now only draw or lose" holds on Hard only; on Easy a win is possible.
- Implementation note: `computer_move(board)` is unchanged (always optimal). New
  `choose_computer_move(board, difficulty, rng)` picks the move for a difficulty; `rng` is a
  `random.Random`-like object (`random()` and `choice()`), passed in so tests can control it.
- Score (R7-R9), undo (R10-R12) and quitting work as before on both difficulties.


## Round 6

Covers R16-R18 from problem.md. Everything in Rounds 1-5 still applies except where noted.

- Score file (decided with the user): `score.json`, in the same folder as `tictactoe.py` (not the
  current working directory, so the score is the same wherever the program is launched).
  Format: a JSON object with exactly three keys, e.g. `{"wins": 2, "losses": 1, "draws": 0}`.
- Saving (R16): after each game ends, the program writes the updated score to the file, before it
  asks "Play again? (y/n)". The file is replaced as a whole each time.
- Mid-game quit (decided with the user): when the player quits mid-game (`q` or end of input), the
  loss recorded by Round 2 is saved too, so the file always matches the final score shown.
- Loading (R17): at startup, before the difficulty prompt, if the file exists and holds a valid
  score, the session score starts from it. R8 and R9 then show scores that include it.
- Valid score (R18, decided with the user, strict): a JSON object whose keys are exactly `wins`,
  `losses` and `draws`, each a whole number >= 0 (a JSON integer; booleans, floats, strings and
  negatives are invalid; extra or missing keys are invalid).
- Missing or invalid file (R18): the score starts at 0/0/0 with no error and the program runs
  normally. Invalid means the file cannot be read, is not JSON, or is not a valid score as above.
  The bad file is left alone until the first save replaces it.
- Save failure (decided with the user): if the file cannot be written, print one line
  `Warning: could not save your score to <path>.` and keep playing; the score stays in memory.
  Saving is attempted again after the next game.
- One combined record: the score is not kept per difficulty.
- Changes earlier behavior: Round 2's "it is not saved between runs" no longer holds. R7's count now
  carries across runs. If the player has played earlier runs, the first score line shown already
  includes those games. The final score of Round 5 with end of input at the difficulty prompt is
  no longer necessarily all zeros: it shows the loaded score.
- Implementation note: `load_score(path)` returns a score dict (the all-zero score for a missing or
  invalid file); `save_score(score, path)` returns True on success and False if it could not write.
  Both take the path as an argument so tests use a temporary folder and never touch the real file.
