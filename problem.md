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

## Round 3 requirements

This round lets the player take back a mistake, such as typing the wrong square number, instead of being stuck with it for the rest of the game.

1. R10: When it is the player's turn, they can type a command (such as undo) instead of a square number to take back their most recent move.
2. R11: Undoing also removes the computer's reply to that move, so the board returns to the state just before the player's last move and it is the player's turn again.
3. R12: If there is nothing to undo (no moves made yet in the current game), the program says so and asks for a square again, and the score is never changed by an undo.

## Round 4 requirements

This round makes the game a real challenge: the player is now up against an opponent that cannot be beaten, so the best outcome is a draw.

### Changed requirement
1. R3 is changed (it keeps its ID and number). Old wording: "The computer opponent takes its turn automatically, always choosing a legal move using a simple strategy." New wording: "The computer opponent takes its turn automatically, always choosing a legal move using optimal play (it never loses)." Only the strategy part changed; the computer still moves automatically and always picks a legal move.

### What this means for earlier requirements
R4, R5, R7, R8 and R11 are unchanged and still apply. With an optimal opponent, the player's results will be draws or losses, and the score from R7 will show that.