# Player Reversi
players of (originally board) two-player game [Reversi](https://en.wikipedia.org/wiki/Reversi)
Player is playing with using alpha-beta pruning

Let's have a square playing area of 8 x 8 square squares. The playing area is bounded and the edges of the playing area are not adjacent to each other. We have playing stones of two colors. At the beginning of the game, we have two stones of each color placed in the center of the board. The player who is on the turn places a stone of his own colour on the board so as to close at least one continuous row of his opponent's stones, ending with his own stone. All of the opponent's stones in continuous rows from the point of placement to the point of your stone then become the player's stones on the turn. It is therefore possible to complete more than one row. This can be done horizontally, vertically and diagonally. If a player cannot place a stone in such a way that the opponent takes at least one stone, the opponent automatically plays. The game ends when the entire board is filled with stones or if no player can place his stone. The winner of the game is the player with more stones on the board than his opponent.

More information about program is [here](https://cw.fel.cvut.cz/b221/courses/b4b33rph/cviceni/reversi/start).
