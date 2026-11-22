# 0006: Save the score as a strictly validated JSON file next to the script, saved after every game

In the context of Round 6 (R16-R18), where the win/loss/draw score must survive between runs and a missing
or unreadable file must never stop the game,
facing the choice of file format, file location, how strict to be when loading, and when to save,
we decided to store `{"wins": n, "losses": n, "draws": n}` as JSON in `score.json` in the same folder as
`tictactoe.py`, to load it with `load_score(path)` and accept it only if it has exactly those three keys, each
a whole number >= 0 (otherwise the all-zero score), to write it with `save_score(score, path)` after every game
(including a mid-game quit, which counts as a loss) before the play-again prompt, and to print a one-line
warning and keep playing if the write fails,
and neglected a plain text file such as `2 1 0`, the `pickle` module, a file in the current working directory
or the user's home folder, lenient loading that keeps whichever fields are valid, and saving only once when
the session ends,
to achieve a file that a person can read and fix by hand, that the standard library parses safely (unlike
`pickle`, which can run code from a tampered file), that is the same wherever the program is launched from,
that never half-loads a damaged score, and that loses at most the game in progress if the window is closed
or the program is killed,
accepting that a damaged file is silently replaced by the next save (the old contents are not backed up),
that `score.json` beside the script is shared by everyone who uses that copy of the program, that a file in
a read-only install folder means the score is not saved (the warning says so), and that a future round that
adds a field to the file must also change the "exactly three keys" rule,
because with a score of three counters, simple and predictable beats clever: a half-trusted file could show a
wrong record, whereas starting from zero is easy to notice and explain (R18).
