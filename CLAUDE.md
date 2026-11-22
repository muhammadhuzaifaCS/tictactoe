# tictactoe: standing rules

## Language
Python 3.11+, standard library only. No third-party packages.

## Run
python tictactoe.py

## Test
python -m unittest. Tests cover board/game logic (win/draw detection, move validation,
computer move strategy) directly, not the interactive input loop.

## Rules
- Keep game logic (board state, win/draw detection, computer strategy) in functions
  separate from the input/print loop, so logic stays unit-testable without mocking stdin.
- Never let invalid input crash the program — always re-prompt.
- Each round's new behavior gets new tests; do not remove a passing test unless the
  requirement it checks was explicitly changed or removed in problem.md.
- Do not add features beyond the current round's requirements in problem.md without
  asking first.
