# 0001: Represent the session score as an immutable dict updated by a pure function

In the context of Round 2 (R7-R9), which needs a running win/loss/draw count that is
shown after every game and again when the player quits,
facing the need to keep game logic unit-testable without mocking stdin (CLAUDE.md rule),
we decided to store the score as a plain dict `{"wins", "losses", "draws"}` and update it
with `record_result(score, result)`, which returns a new dict instead of changing the old one,
and neglected a `Score` class with mutating methods, and a module-level global counter,
to achieve logic that matches the existing style (`make_move` also returns a new board)
and can be tested with plain values,
accepting that the main loop must reassign `score = record_result(score, ...)` each game
and that a typo in a key name is only caught at runtime, not by a class definition,
because a three-field counter does not justify a class in a standard-library-only project.
