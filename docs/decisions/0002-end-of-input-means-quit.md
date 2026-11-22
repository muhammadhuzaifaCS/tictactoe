# 0002: Treat end of input as quitting at both prompts

In the context of the new play-again re-prompt (invalid answers ask again) and the CLAUDE.md
rule that the program must never crash on input,
facing the problem that when stdin closes (Ctrl-D / Ctrl-Z, or piped input running out)
`input()` raises `EOFError`, and a re-prompting loop would either crash or spin forever,
we decided to wrap `input()` in `read_line`, which returns `None` at end of input, and to
treat `None` as quit at the move prompt (counts as a loss, like `q`) and at the play-again prompt,
and neglected letting `EOFError` propagate (traceback on Ctrl-D), and treating end of input
at the move prompt as "abandon without scoring",
to achieve a program that always exits cleanly with the final score shown,
accepting that closing the input mid-game records a loss, consistent with `q`,
because one rule ("leaving a game early is a loss") is simpler to explain than two.
