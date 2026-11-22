# Handoff: end of Round 2

For a fresh session starting Round 3. Read this, then `problem.md`, `spec.md`, `CLAUDE.md`
and `docs/decisions/` before doing anything.

## Current state

- Terminal tic-tac-toe, Python 3.11+, standard library only. Human is `X` and moves first;
  computer is `O`.
- Rounds 1 and 2 are done and committed on `master`. Last commit when this was written:
  `9224c30`. All 42 tests pass.
- Requirements covered: R1-R6 (Round 1: board, input, computer opponent, win/draw, play
  again) and R7-R9 (Round 2: session score, score shown after each game, play until quit
  with a final score).
- Files: `tictactoe.py` (everything), `test_tictactoe.py`, `spec.md` (cumulative; Round 1
  and Round 2 sections), `problem.md`, `README.md`, `docs/decisions/0001-*.md` and
  `0002-*.md`.
- Nothing is pushed. The branch is ahead of `origin/master`.

## Run and test

```
python tictactoe.py
python -m unittest
```

Run both from this directory (`final-project/tictactoe`).

## How the code is laid out

- Pure logic functions at the top (board, win/draw, computer move, `game_result`,
  `record_result`, `format_score`, `parse_yes_no`, `is_quit_command`). These are the tested part.
- Below a comment divider: the input/print loop (`read_line`, `prompt_human_move`,
  `prompt_play_again`, `play_one_game`, `main`). Not unit-tested, by design (CLAUDE.md).
- Score is a dict `{"wins", "losses", "draws"}` from the human's point of view. It lives
  only in memory for one run.

## Decisions made in Round 2, and why

Asked of the user and answered:
- Invalid answer at "Play again? (y/n)" re-prompts (it used to quit). Reason: R9 says
  "until the player chooses to quit", so a typo should not count as choosing.
- `q` at the move prompt quits the session, and the unfinished game counts as a loss.
  The user chose this over "not counted" and over "no mid-game quit".

Made without asking (the user was told):
- Score is an immutable dict updated by `record_result` (`docs/decisions/0001`).
- End of input (`EOFError`) means quit at both prompts; mid-game it records a loss
  (`docs/decisions/0002`). Without this, re-prompting would loop forever on closed stdin.
- Only `y`/`n` accepted at play-again (not `yes`/`no`); only `q` quits mid-game (not `quit`).
- Score line format: `Score - Wins: 2  Losses: 1  Draws: 0`; final: `Final score - ...`.

## Unresolved / loose ends

- Round 1 tests do not name requirement IDs; only Round 2 tests do (`test_R7_...`). Left
  alone because renaming tests was not requested.
- `__pycache__/` is untracked and there is no `.gitignore`. Not added because nobody asked.
- `README.md` was not updated for Round 2 (it does not mention score or `q`).
- The input/print loop (`main`, `play_one_game`) has no automated test. Only manual runs
  with piped input.
- Mid-game quit counting as a loss is a user choice that may be revisited.

## Warnings

- When writing Python or text files through shell heredocs, `\n` sequences in strings were
  turned into real line breaks in this environment, which broke `tictactoe.py` and one
  test file. Use the Write/Edit tools for code, and run `python -m unittest` straight after.
- Git prints "LF will be replaced by CRLF" warnings on Windows. They are harmless.
- The parent repo `CLAUDE.md` (course repo) says to commit by default and to re-fetch
  course instructions at session start. This project's prompts so far have also said when
  not to commit (for example, this handoff file). Follow the most recent explicit user
  instruction.
- `problem.md` and the prompt for each round define scope. Do not add features beyond
  the current round without asking.
- Never undo or amend a commit. Fix mistakes with a new commit.
