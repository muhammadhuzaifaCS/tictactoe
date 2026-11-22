# Problem

Someone with a few spare minutes, such as a student on a study break or a friend waiting around with no one to play against, wants a quick game of tic-tac-toe. They are already at a computer with a terminal open, but they have no second player and don't want to open a browser or install a game just for a short match.

## Initial requirements

1. R1: The program shows the 3x3 board in the terminal at the start of the game and after every move.
2. R2: The human player picks a square by typing its position, and the program rejects invalid input or an already-taken square and asks again.
3. R3: The computer opponent takes its turn automatically, always choosing a legal move using a simple strategy.
4. R4: The program detects when either player has three in a row and announces the winner.
5. R5: The program detects a full board with no winner and announces a draw.
6. R6: When a game ends, the player can choose to play again or quit.


## Round 2 requirements

This round turns a single game into a session: the player keeps a running score against the computer instead of starting from zero every time.

1. R7: The program keeps a running count of the player's wins, losses, and draws across all games in the current session.
2. R8: After each game ends, the program shows the updated score before asking whether to play again.
3. R9: The program keeps starting new games until the player chooses to quit, and shows the final score when they do.