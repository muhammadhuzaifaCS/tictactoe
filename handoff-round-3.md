# Handoff: end of Round 3

For a fresh session starting Round 4. Read this, then `problem.md`, `spec.md`, `CLAUDE.md`
and `docs/decisions/` before doing anything. This supersedes `handoff-round-2.md`, which is
still useful background.

## Current state

- Terminal tic-tac-toe, Python 3.11+, standard library only. Human is `X` and moves first;
  computer is `O`.
- Rounds 1-3 are done and committed on `master`. Last commit when this was written: `ce45972`.
  All 53 tests pass. The working tree was clean apart from this file and the `CLAUDE.md`
  edit, which are uncommitted on purpose (the user reviews them first).
- Requirements covered: R1-R6 (board, input, computer opponent, win/draw, play again),
  R7-R9 (session score, score after each game, play until quit), R10-R12 (undo).
- Files: `tictactoe.py` (everything), `test_tictactoe.py`, `spec.md` (cumulative, one section
  per round), `problem.md`, `README.md`, `docs/decisions/0001`-`0003`.
- Nothing is pushed.

## Run and test

```
python tictactoe.py
python -m unittest
```

Run both from this directory (`final-project/tictactoe`). A quick manual check with piped
input works: `printf 'u\n1\nu\nq\n' | python tictactoe.py`.

## How the code is laid out

- Pure logic at the top: board, win/draw, `computer_move`, `game_result`, `record_result`,
  `format_score`, `parse_yes_no`, `is_quit_command`, and (Round 3) `is_undo_command` and
  `undo_move`. These are the tested part.
- Below a comment divider is the input/print loop: `read_line`, `prompt_human_move`,
  `prompt_play_again`, `play_one_game`, `main`. Not unit-tested, by design (CLAUDE.md).
- `prompt_human_move` returns a 1-9 int, `QUIT` or `UNDO` (string constants).
- `play_one_game` keeps `history`, a list of boards snapshotted just before each player move.
  Undo pops the last snapshot, which removes the player's move and the computer's reply.
- Score is a dict `{"wins", "losses", "draws"}`, human's point of view, in memory only.

## Decisions made in Round 3, and why

Asked of the user and answered:
- Undo command is `undo` or `u` (trimmed, any case).
- Undo is unlimited: each undo steps back one more player+computer pair until the board is empty.
- The move prompt mentions undo: `Your move (1-9, u to undo, or q to quit): `.

Made without asking (the user was told):
- History is board snapshots with a pure `undo_move(history)` (`docs/decisions/0003`).
- History is per game, so undo never reaches into a previous game.
- The "invalid input" message also mentions undo.
- After an undo the program prints "Undid your last move and the computer's reply." and the
  restored board; with nothing to undo it prints "Nothing to undo."
- `UNDO = "undo"` constant, mirroring `QUIT`.
- One line about undo was added to `README.md`.

## Unresolved / loose ends

- Round 1 tests still do not name requirement IDs (Rounds 2 and 3 do). CLAUDE.md says every
  requirement test names its ID; the old tests predate that rule. Not renamed because nobody asked.
- `__pycache__/` is untracked and there is no `.gitignore`. Not added because nobody asked.
- The input/print loop (`play_one_game`, `main`) has no automated test, so the wiring of
  undo (R10-R12 in the real loop) was only checked by hand with piped input.
- Mid-game quit counting as a loss is a user choice from Round 2 and may be revisited.
- `spec.md` mentions the invalid-input message wording; keep it in sync if prompts change.

## Warnings

- Shell heredocs and `python -` scripts expanded `\n` inside strings into real line breaks
  in Rounds 2 and 3, breaking a test file both times. Use the Write/Edit tools for code, and
  run `python -m unittest` straight after. This is now in CLAUDE.md as a standing rule.
- In Round 3 the failing-tests commit contained that syntax error; it was fixed in the next
  commit. Check that test files at least import before committing them.
- Git prints "LF will be replaced by CRLF" warnings on Windows. They are harmless.
- The parent repo `CLAUDE.md` (course repo) says to commit by default and to re-fetch course
  instructions at session start. This project's prompts say when not to commit (for example
  this handoff and `CLAUDE.md`). Follow the most recent explicit user instruction.
- `problem.md` and each round's prompt define scope. Do not add features beyond the current
  round without asking, and ask about ambiguous requirements before writing code.
- Never undo or amend a commit. Fix mistakes with a new commit.
