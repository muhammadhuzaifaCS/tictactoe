# 0004: Make the computer unbeatable with full minimax, preferring quick wins and the lowest square on ties

In the context of Round 4, where R3 changes from "simple strategy" to "optimal play (it never loses)",
facing the choice of how to build an opponent that cannot lose and how to pick among moves that are
equally good,
we decided to search the whole game tree with minimax (the computer maximizes, the human minimizes),
to score a win as `10 - depth` and a loss as `depth - 10` so that quicker wins and slower losses are
preferred, to cache results with `functools.lru_cache`, and to break remaining ties by taking the
lowest-numbered square,
and neglected extending the old rule list (win, block, center, corner, side) with a fork check,
a hard-coded opening book, and picking randomly among equal moves,
to achieve a computer that is correct by construction (tic-tac-toe has under 550,000 move sequences, so
searching everything is fast), that finishes games in the fewest moves, and that always gives the same
reply to the same board, which keeps tests and undo (R11) predictable,
accepting that the computer is always deterministic and so the game plays out the same way every time
against the same moves, and that `_minimax` takes a tuple instead of a list so it can be cached,
because patching the old rule list leaves room for missed cases such as forks, which a test can only
sample but a full search covers, and randomness would make "never loses" and the tests harder to check.
