# Handoff: end of Round 4

For a fresh session starting Round 5. Read this, then `problem.md`, `spec.md`, `CLAUDE.md`
and `docs/decisions/` before doing anything. This supersedes `handoff-round-3.md`; the Round 2
and 3 handoffs are still background.

## Current state

- Terminal tic-tac-toe, Python 3.11+, standard library only. Human is `X` and moves first;
  computer is `O`.
- Rounds 1-4 are done and committed on `master`. Last commit when this was written: `64d093d`.
  All 62 tests pass. The working tree was clean apart from this file and the `CLAUDE.md`
  edit, which are uncommitted on purpose (the user reviews them first).
- Requirements covered: R1-R6 (board, input, computer opponent, win/draw, play again),
  R7-R9 (session score), R10-R12 (undo). Round 4 changed only R3: the computer now plays
  optimally (minimax) and never loses, so the player's best result is a draw.
- Files: `tictactoe.py` (everything), `test_tictactoe.py`, `spec.md` (cumulative, one section
  per round), `problem.md`, `README.md`, `docs/decisions/0001`-`0004`.
- Nothing is pushed.

## Run and test

```
python tictactoe.py
python -m unittest
```

Run both from this directory (`final-project/tictactoe`). The test run takes well under a
second. A quick manual check with piped input works:
`printf '5\n1\n9\n2\n7\n6\n3\n4\n8\nn\n' | python tictactoe.py` plays a full drawn game.

## How the code is laid out

- Pure logic at the top: board, win/draw, `_minimax` and `computer_move`, `game_result`,
  `record_result`, `format_score`, `parse_yes_no`, `is_quit_command`, `is_undo_command`,
  `undo_move`. These are the tested part.
- `_minimax(board_tuple, mark_to_move, depth)` is cached with `lru_cache`, so it takes a tuple,
  not a list. `computer_move(board)` takes a normal list and converts.
- Below a comment divider is the input/print loop: `read_line`, `prompt_human_move`,
  `prompt_play_again`, `play_one_game`, `main`. Not unit-tested, by design (CLAUDE.md).
- Score is a dict `{"wins", "losses", "draws"}`, human's point of view, in memory only.
  Undo history is a list of board snapshots, per game.

## Decisions made in Round 4, and why

Asked of the user: none. The prompt had no unclear requirement, so none were asked; the user
was told the choices below at the end of the round. Revisit any of them if the user objects.

- Minimax over the full game tree, not an extended rule list (`docs/decisions/0004`): correct
  by construction, and the whole tree is small.
- Quicker wins and slower losses are preferred (score is `10 - depth` / `depth - 10`).
- Ties go to the lowest-numbered square, so the computer is deterministic. Side effect: it
  always opens at square 1 if it ever moves first, and redoing a move after an undo gets the
  same reply.
- `lru_cache` on the search (4.4s down to 0.06s for the tests).
- Removed the now-unused `CORNERS`, `SIDES`, `CENTER` constants.
- Replaced `test_takes_center_when_open_and_no_win_or_block` (it only checked the old
  strategy). Renamed the four other computer-move tests to carry `R3`.
- Added tests: exhaustive "never loses" over every human line, "can still draw / can still
  win", corner opening gets the center, opposite-corners trap, fastest win, no mutation, full
  board raises, deterministic reply.
- `README.md` and the module docstring now say the computer is unbeatable; `spec.md` has a
  Round 4 section noting that the Round 1 priority list no longer applies.

## Unresolved / loose ends

- Round 1 tests (17 of them, everything except R3 and later) still do not name requirement IDs.
  CLAUDE.md says every requirement test names its ID. Not renamed because nobody asked.
- The input/print loop (`play_one_game`, `main`) has no automated test; wiring was only checked
  by hand with piped input.
- Mid-game quit counting as a loss is a user choice from Round 2 and may be revisited. With an
  unbeatable opponent, losses will be common, so this may feel harsher now.
- Because the computer never loses and is deterministic, the same sequence of human moves always
  produces the same game. Any later round that wants variety (levels, randomness) is a new
  requirement; ask first.
- `spec.md` mentions the invalid-input message wording; keep it in sync if prompts change.

## Warnings

- Do not write code or tests with shell heredocs or `python -` scripts with `\n` in strings, and
  avoid `sed -i` on code. In Round 4 a `sed -i` added a duplicate import to the test file (harmless
  but wrong). This is in CLAUDE.md now. Run `python -m unittest` right after writing.
- The shell is Git Bash, but the harness default shell may be PowerShell; write Bash syntax.
- `git add` with the pathspec `':!__pycache__'` fails in this Git ("Unimplemented pathspec
  magic"). Add files by name. `.gitignore` already covers `__pycache__/`.
- Git prints "LF will be replaced by CRLF" warnings on Windows. They are harmless.
- The editor may report a file "changed on disk" after a shell edit. Re-read before editing it.
- The parent repo `CLAUDE.md` (course repo) says to commit by default and to re-fetch course
  instructions at session start. This project's prompts say when not to commit (for example this
  handoff and `CLAUDE.md`). Follow the most recent explicit user instruction.
- `problem.md` and each round's prompt define scope. Do not add features beyond the current round
  without asking, and ask about ambiguous requirements before writing code.
- Never undo or amend a commit. Fix mistakes with a new commit.
