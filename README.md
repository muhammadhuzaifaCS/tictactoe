# tictactoe

Terminal tic-tac-toe against the computer, on Easy (it sometimes plays a random move, so you
can win) or Hard (unbeatable, the best you can do is draw), with a running win/loss/draw score
across games in a session. See `problem.md` for the problem and requirements, `spec.md`
for the current round's exact behavior, and `docs/decisions/` for why specific choices
were made.

## Run

```
python tictactoe.py
```

At the start, type `easy` or `hard` (once; it applies to every game in the session). Then type a
square number (1-9) to move, `u` (or `undo`) to take back your last move and the
computer's reply, or `q` to quit mid-game. After each game, the score
is shown and you're asked to play again (`y`/`n`); the final score is shown when you quit.

Your score is saved to `score.json` (next to `tictactoe.py`) after every game and loaded the next time you
start, so your record carries over between runs. If the file is missing or damaged, the score starts at 0.
Delete `score.json` to reset it.

## Test

```
python -m unittest
```

(Tests cover board/game logic directly — win/draw detection, move validation, and the
computer's optimal-play strategy — not the interactive input loop.)
