# Handoff: end of Round 6

For a fresh session starting Round 7. Read this, then `problem.md`, `spec.md`, `CLAUDE.md` and
`docs/decisions/` before doing anything. This supersedes `handoff-round-5.md`; older handoffs are
background only.

## Current state

- Terminal tic-tac-toe, Python 3.11+, standard library only. Human is `X` and moves first; computer
  is `O`.
- Rounds 1-6 are done and committed on `master`. Last commit when this was written: `ca5bce4`.
  All 107 tests pass (79 before Round 6, 28 new).
- Requirements covered: R1-R6 (board, input, computer, win/draw, play again), R7-R9 (session score),
  R10-R12 (undo), R3 changed in Round 4 (optimal play), R13-R15 (Easy/Hard), R16-R18 (saved score).
- Files: `tictactoe.py` (everything), `test_tictactoe.py`, `spec.md` (cumulative, one section per
  round), `problem.md`, `README.md`, `docs/decisions/0001`-`0006`, handoff files, `.gitignore`.
- Uncommitted on purpose (the user reviews them first): this file and the `CLAUDE.md` edit (three new
  rules at the end of the Rules list). Nothing is pushed.

## Run and test

```
python tictactoe.py
python -m unittest
```

Run both from this directory (`final-project/tictactoe`). Tests take about 0.2 s. Manual check with
piped input: `printf 'hard\n5\n1\n9\n2\n7\n6\n3\n4\n8\nn\n' | python tictactoe.py` plays a drawn game
on Hard. **The program now writes `score.json` next to `tictactoe.py`.** It is git-ignored, but delete
it after manual runs so the next session starts from a known score (or the next run shows an old one).

## How the code is laid out

- Pure logic at the top: board, win/draw, `_minimax` and `computer_move` (always optimal, cached),
  score functions, `parse_yes_no`, `is_quit_command`, `is_undo_command`, `undo_move`, the Round 5
  block (`EASY`, `HARD`, `parse_difficulty`, `choose_computer_move(board, difficulty, rng)`), and the
  Round 6 block: `SCORE_FILE`, `_is_valid_score`, `load_score(path)`, `save_score(score, path)`.
- Below the comment divider is the input/print loop: `read_line`, the prompts, `play_one_game`,
  `save_score_or_warn(score, path=SCORE_FILE)`, `main`. Not unit-tested, by design (CLAUDE.md).
- `main` loads the score first, asks for difficulty once, then loops games. After each finished game
  it records the result, saves, shows the score, then asks to play again. A mid-game quit records the
  loss, saves, and exits.
- Score is a dict `{"wins", "losses", "draws"}` from the human's point of view. Undo history is a list
  of board snapshots, per game.

## Decisions made in Round 6, and why

Asked of the user (answers are in `spec.md`, Round 6):
- File: `score.json` in the same folder as `tictactoe.py` (not the working directory), JSON.
- Strict validation: exactly the keys `wins`, `losses`, `draws`, each a whole number >= 0; anything
  else starts at 0/0/0.
- A mid-game quit (`q` or end of input) saves its loss too.
- A failed save prints one warning line and the game continues.

Made without asking (listed to the user at the end of the round; revisit if they object):
- Save happens before the "Play again?" prompt, so closing the window loses nothing (decision 0006).
- JSON booleans and floats such as `2.0` are rejected as counts; unreadable, non-UTF-8 and non-JSON
  files count as invalid. `RecursionError` from a deeply nested file is also caught.
- An invalid file is left untouched at load; the next save replaces it with no backup.
- Warning text: `Warning: could not save your score to <path>.` (full path). It repeats after every
  later game while saving keeps failing.
- `score.json` was added to `.gitignore`; `README.md` has a short paragraph about it.
- Decision record `0006` covers format, location, strictness and timing (alternatives rejected: plain
  text, `pickle`, working directory or home folder, lenient field-by-field loading, save only at exit).
- Only `load_score` and `save_score` have tests. They use `tempfile` and the real `score.json` is
  never touched. No earlier test was removed or changed.

## Unresolved / loose ends

- Round 1 tests (17 of them) still do not name requirement IDs, against CLAUDE.md. Not renamed
  because nobody asked.
- The input/print loop has no automated test. These were checked only by hand with piped input:
  R13 (difficulty asked once), the main-loop save timing, the mid-game-quit save, the save-failure
  warning, and "loaded score appears in the first score line".
- The score is one combined record, not per difficulty (stated in problem.md). Easy wins and Hard
  draws mix in the same file.
- No file locking: two copies of the game running at once overwrite each other's score.
- Mid-game quit counts as a loss (a Round 2 choice); it now also writes to disk. Not revisited.
- Spec note: the Round 5 line "end of input at the difficulty prompt prints an all-zero final score"
  is superseded: it prints the loaded score. That is recorded in the Round 6 section of `spec.md`.

## Warnings

- Write code and tests with Write/Edit, never shell heredocs or `python -` scripts with `\n` in
  strings, and avoid `sed -i` on code (see CLAUDE.md). Run `python -m unittest` right after writing.
- Before committing a "failing tests" step, check every new test fails by assertion. Use stubs that
  are wrong and have the forbidden side effects (see the new CLAUDE.md rule); a do-nothing stub let
  4 tests pass in Round 6.
- The harness default shell may be PowerShell; write Bash syntax. The course repo says to use Git Bash.
- `git add` with the pathspec `':!__pycache__'` fails in this Git. Add files by name.
- Git prints "LF will be replaced by CRLF" warnings on Windows. They are harmless.
- The editor may report a file "changed on disk" after a shell edit. Re-read before editing it.
- The parent repo `CLAUDE.md` (course repo) says to commit by default and to re-fetch course
  instructions at session start. This project's prompts say when not to commit (for example the
  handoff and `CLAUDE.md`). Follow the most recent explicit user instruction.
- `problem.md` and each round's prompt define scope. Do not add features beyond the current round
  without asking, and ask about ambiguous requirements before writing code.
- Any future change to the score file's fields must also change the "exactly three keys" rule in
  `_is_valid_score`, `spec.md` and decision 0006 (old files would otherwise load as invalid and
  silently reset the score to zero).
- Never undo or amend a commit. Fix mistakes with a new commit.
