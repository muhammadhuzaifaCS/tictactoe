# Handoff: end of Round 5

For a fresh session starting Round 6. Read this, then `problem.md`, `spec.md`, `CLAUDE.md` and
`docs/decisions/` before doing anything. This supersedes `handoff-round-4.md`; the older handoffs
are background only.

## Current state

- Terminal tic-tac-toe, Python 3.11+, standard library only. Human is `X` and moves first;
  computer is `O`.
- Rounds 1-5 are done and committed on `master`. Last commit when this was written: `0096261`.
  All 79 tests pass.
- Requirements covered: R1-R6 (board, input, computer, win/draw, play again), R7-R9 (session
  score), R10-R12 (undo), R3 changed in Round 4 (optimal play), R13-R15 (Easy/Hard difficulty).
- Files: `tictactoe.py` (everything), `test_tictactoe.py`, `spec.md` (cumulative, one section per
  round), `problem.md`, `README.md`, `docs/decisions/0001`-`0005`, handoff files.
- Uncommitted on purpose (the user reviews them first): this file and the `CLAUDE.md` edit
  (two new rules at the end of the Rules list). Nothing is pushed.

## Run and test

```
python tictactoe.py
python -m unittest
```

Run both from this directory (`final-project/tictactoe`). Tests take about 0.1 s. Manual check with
piped input: `printf 'hard\n5\n1\n9\n2\n7\n6\n3\n4\n8\nn\n' | python tictactoe.py` plays a drawn
game on Hard. The first line is the difficulty answer; it is asked once per session.

## How the code is laid out

- Pure logic at the top: board, win/draw, `_minimax` and `computer_move` (always optimal, cached),
  score functions, `parse_yes_no`, `is_quit_command`, `is_undo_command`, `undo_move`, and the
  Round 5 block: `EASY`, `HARD`, `EASY_RANDOM_CHANCE`, `parse_difficulty`,
  `choose_computer_move(board, difficulty, rng)`.
- Below the comment divider is the input/print loop: `read_line`, `prompt_human_move`,
  `prompt_difficulty`, `prompt_play_again`, `play_one_game(difficulty=HARD, rng=random)`, `main`.
  Not unit-tested, by design (CLAUDE.md).
- `main` asks for difficulty once, then loops games while `difficulty is not None`.
- Score is a dict `{"wins", "losses", "draws"}` from the human's point of view, in memory only.
  Undo history is a list of board snapshots, per game.

## Decisions made in Round 5, and why

Asked of the user: none. Nothing in R13-R15 was unclear enough to block, so the choices below were
made and listed at the end of the round. Revisit any if the user objects.

- Easy = a 1/3 chance of a uniformly random legal move, otherwise optimal (`docs/decisions/0005`).
  `computer_move` is untouched, so Hard and all Round 4 tests are unchanged. A depth-limited
  minimax or a second hand-written strategy was rejected because their mistake rate could not be
  stated or tested as "about one in three".
- The random source is passed in as `rng` (a `random.Random` in the real game, a fixed fake
  `FixedRng` in tests), so tests need no patching.
- Difficulty answers: `easy`/`e` and `hard`/`h`, trimmed, any case. Anything else prints
  "Please answer easy or hard." and re-asks.
- End of input at the difficulty prompt exits cleanly with the all-zero final score (decision 0002).
  `q` there is just an invalid answer, not a quit.
- The dice are rolled fresh every computer turn. A random move can equal the optimal one, so the
  real mistake rate is a bit under 1/3.
- Unknown difficulty passed to `choose_computer_move` raises `ValueError`.
- `spec.md` notes that Round 4's "same board, same reply" and "player can only draw or lose" now
  hold on Hard only; on Easy an undo-and-redo can get a different computer reply.
- No earlier test was removed or replaced. 17 new tests carry R13/R14/R15 in their names.

## Unresolved / loose ends

- Round 1 tests (17 of them) still do not name requirement IDs, against CLAUDE.md. Not renamed
  because nobody asked.
- The input/print loop has no automated test. "The difficulty is asked once and kept across games"
  (R13) was only checked by hand with piped input.
- Mid-game quit counts as a loss (a Round 2 user choice). It may feel harsh on Hard; not revisited.
- A Round 5 bug in a test was caught only because stubs were used: one new test passed against the
  placeholder. That is now a CLAUDE.md rule.
- The difficulty is per session and in memory only; nothing is saved between runs.

## Warnings

- Write code and tests with Write/Edit, never shell heredocs or `python -` scripts with `\n` in
  strings, and avoid `sed -i` on code (see CLAUDE.md). Run `python -m unittest` right after writing.
- The harness default shell may be PowerShell; write Bash syntax. The course repo says to use Git Bash.
- `git add` with the pathspec `':!__pycache__'` fails in this Git. Add files by name.
  `.gitignore` already covers `__pycache__/`.
- Git prints "LF will be replaced by CRLF" warnings on Windows. They are harmless.
- The editor may report a file "changed on disk" after a shell edit. Re-read before editing it.
- The parent repo `CLAUDE.md` (course repo) says to commit by default and to re-fetch course
  instructions at session start. This project's prompts say when not to commit (for example the
  handoff and `CLAUDE.md`). Follow the most recent explicit user instruction.
- `problem.md` and each round's prompt define scope. Do not add features beyond the current round
  without asking, and ask about ambiguous requirements before writing code.
- Never undo or amend a commit. Fix mistakes with a new commit.
