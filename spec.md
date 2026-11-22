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
  (or anything else) exits.
