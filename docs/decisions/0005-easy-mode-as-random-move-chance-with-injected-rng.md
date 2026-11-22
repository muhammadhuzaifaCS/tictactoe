# 0005: Build Easy mode as a one-in-three chance of a random move, with the random source passed in

In the context of Round 5 (R13-R15), where the player picks Easy or Hard and Easy must "sometimes
make mistakes" about one turn in three while Hard stays the unbeatable Round 4 computer,
facing the choice of how to make the computer weaker and how to keep that testable without mocking,
we decided to leave `computer_move` untouched (always optimal) and add
`choose_computer_move(board, difficulty, rng)`, which on Easy rolls `rng.random()` and, below 1/3,
plays `rng.choice` of the legal squares, otherwise calls `computer_move`, with `rng` passed in
(a `random.Random` in the real game, a fixed fake in tests),
and neglected a weaker search (minimax limited to a shallow depth), a separate hand-written "simple
strategy" like Round 1's priority list, and calling the global `random` module directly inside the logic,
to achieve an Easy mode that matches the wording of R15 exactly (a measurable one-in-three chance, optimal
otherwise), keeps Hard and all Round 4 tests and decisions unchanged, and lets tests control the dice
(force a mistake, force the optimal move, check the 1/3 boundary) with no patching of `random`,
accepting that a random move can coincide with the optimal one (so the real mistake rate is a bit under 1/3),
that Easy is no longer deterministic (so undo, R11, can give a different reply after a redo), and that
`play_one_game` and `choose_computer_move` carry an extra `rng` argument,
because R15 describes a probability, not a skill level, and a depth limit or a second strategy would
produce mistakes whose frequency nobody could state or test as "about one in three".
