# 0003: Implement undo with a list of board snapshots taken before each player move

In the context of Round 3 (R10-R12), which lets the player take back their last move together
with the computer's reply, repeatedly if wanted,
facing the need to restore the board exactly and keep the logic unit-testable without mocking stdin,
we decided to keep `history`, a list of full board snapshots (one pushed just before each player
move), and to undo with the pure function `undo_move(history)`, which returns the previous board
and the shorter history, or `None` when empty,
and neglected recomputing the board by removing the last two marks from the current board, and
storing the list of moves and replaying them from an empty board,
to achieve an undo that cannot drift out of sync with the board (it restores a stored state, so it
works the same whatever the computer strategy does) and that matches the existing immutable style
(`make_move`, `record_result` also return new values),
accepting that each turn stores one extra 9-element list (negligible for a 9-square game),
because removing "the last two marks" would need to know which squares those were, and a replay
would need a move list that nothing else uses.
