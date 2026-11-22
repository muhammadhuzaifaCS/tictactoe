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
- Every test for a requirement names its ID (e.g. `test_R7_...`).
- Record each significant decision that had real alternatives as a Y-statement in
  docs/decisions/, numbered 0001, 0002, ... (continue the numbering; never reuse one).
- Keep spec.md current: add a section per round, and note any earlier behavior a round changes.
- Never undo or amend a commit; fix mistakes with a new commit.
- Do not write the handoff file or commit it unless the user asks.
- Write code and test files with the Write/Edit tools, never shell heredocs or `python -`
  scripts with `\n` in strings: the shell expands `\n` into real line breaks and breaks
  string literals (happened in Rounds 2 and 3). Run `python -m unittest` right after writing.
  The same goes for `sed -i` on code or tests: in Round 4 it added a duplicate import.
- Before committing a "failing tests" step, check the tests fail by assertion (the behavior
  is missing), not by an import error or syntax error.
- When a round changes a requirement, tests for it that are still valid stay (rename them to
  carry the ID); a test that only checked the old behavior may be replaced. Say which in the
  end-of-round list of decisions.
- If a requirement is ambiguous, ask the user and wait before writing code.
- When placeholder stubs are added so new tests fail by assertion, run the suite and check
  that every new test fails. A new test that passes against a stub is not testing the
  requirement (in Round 5 one passed because the test overwrote a taken square); fix it first.
- Randomness in game logic takes a `random.Random`-like `rng` argument (needs `random()` and
  `choice()`), so tests pass a fixed fake. Do not patch the global `random` module in tests.
