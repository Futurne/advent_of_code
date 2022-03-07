"""--- Day 21: Dirac Dice ---

There's not much to do as you slowly descend to the bottom of the ocean. The submarine computer challenges you to a nice game of Dirac Dice.
This game consists of a single die, two pawns, and a game board with a circular track containing ten spaces marked 1 through 10 clockwise.
Each player's starting space is chosen randomly (your puzzle input). Player 1 goes first.
Players take turns moving. On each player's turn, the player rolls the die three times and adds up the results.
Then, the player moves their pawn that many times forward around the track (that is, moving clockwise on spaces in order of increasing value, wrapping back around to 1 after 10).
So, if a player is on space 7 and they roll 2, 2, and 1, they would move forward 5 times, to spaces 8, 9, 10, 1, and finally stopping on 2.
After each player moves, they increase their score by the value of the space their pawn stopped on.
Players' scores start at 0. So, if the first player starts on space 7 and rolls a total of 5, they would stop on space 2 and add 2 to their score (for a total score of 2).
The game immediately ends as a win for any player whose score reaches at least 1000.
Since the first game is a practice game, the submarine opens a compartment labeled deterministic dice and a 100-sided die falls out.
This die always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over at 1 again. Play using this die.

For example, given these starting positions:

Player 1 starting position: 4
Player 2 starting position: 8

This is how the game would go:

    Player 1 rolls 1+2+3 and moves to space 10 for a total score of 10.
    Player 2 rolls 4+5+6 and moves to space 3 for a total score of 3.
    Player 1 rolls 7+8+9 and moves to space 4 for a total score of 14.
    Player 2 rolls 10+11+12 and moves to space 6 for a total score of 9.
    Player 1 rolls 13+14+15 and moves to space 6 for a total score of 20.
    Player 2 rolls 16+17+18 and moves to space 7 for a total score of 16.
    Player 1 rolls 19+20+21 and moves to space 6 for a total score of 26.
    Player 2 rolls 22+23+24 and moves to space 6 for a total score of 22.

...after many turns...

    Player 2 rolls 82+83+84 and moves to space 6 for a total score of 742.
    Player 1 rolls 85+86+87 and moves to space 4 for a total score of 990.
    Player 2 rolls 88+89+90 and moves to space 3 for a total score of 745.
    Player 1 rolls 91+92+93 and moves to space 10 for a final score, 1000.

Since player 1 has at least 1000 points, player 1 wins and the game ends.
At this point, the losing player had 745 points and the die had been rolled a total of 993 times; 745 * 993 = 739785.
Play a practice game using the deterministic 100-sided die.
The moment either player wins, what do you get if you multiply the score of the losing player by the number of times the die was rolled during the game?

--- Part Two ---

Now that you're warmed up, it's time to play the real game.
A second compartment opens, this time labeled Dirac dice. Out of it falls a single three-sided die.
As you experiment with the die, you feel a little strange.
An informational brochure in the compartment explains that this is a quantum die: when you roll it,
the universe splits into multiple copies, one copy for each possible outcome of the die.
In this case, rolling the die always splits the universe into three copies: one where the outcome of the roll was 1, one where it was 2, and one where it was 3.
The game is played the same as before, although to prevent things from getting too far out of hand, the game now ends when either player's score reaches at least 21.
Using the same starting positions as in the example above, player 1 wins in 444356092776315 universes, while player 2 merely wins in 341960390180808 universes.
Using your given starting positions, determine every possible outcome. Find the player that wins in more universes; in how many universes does that player win?
"""
import itertools
import numpy as np


def read_input(path: str) -> tuple:
    with open(path, 'r') as input_file:
        lines = input_file.readlines()
        lines = [l.rstrip() for l in lines]

    pos = tuple(
        int(l.split(': ')[-1])
        for l in lines
    )

    return pos


def determinist_dice(pos: tuple) -> int:
    pos = [
        p - 1
        for p in pos
    ]

    scores = [0, 0]

    move = 6
    player_turn = 0

    for n_turns in itertools.count(1):
        pos[player_turn] = (pos[player_turn] + move) % 10
        scores[player_turn] += pos[player_turn] + 1

        if scores[player_turn] >= 1000:
            break

        move = (move - 1) % 10
        player_turn = 1 - player_turn

    n_rolls = n_turns * 3
    return n_rolls * scores[1 - player_turn]


def roll_quantum(pos: np.ndarray, axis: int) -> np.ndarray:
    n_pos = [
        np.roll(pos, dice_value, axis=axis)
        for dice_value in range(1, 4)
    ]
    return sum(n_pos)


def play_one_turn(
        S: np.ndarray,
        P: np.ndarray,
        M: np.ndarray,
    ) -> tuple:
    S = S.reshape(*S.shape, 1)  # Unsqueeze last dim for broadcast
    S = S * P  # [n_scores, n_pos, n_pos]  =>  S[i, j, k] = "how many universes move from pos j to pos k with initial score i"
    S = S.sum(axis=-2)  # [n_scores, n_pos]  => S[i, j] = "how many universes with initial score i are now in pos j"
    for col_idx, shift in enumerate(range(1, 11)):
        S[:, col_idx] = np.roll(S[:, col_idx], shift)  # Move universes to dedicated score

    n_wins = np.sum(S * M)  # Count ended games
    S = (1 - M) * S  # Remove ended games
    return S, n_wins

def quantum_dice(pos: tuple) -> int:
    scores = np.zeros((2, 21, 10), dtype=int)
    scores[0, 0, pos[0] - 1] = 1
    scores[1, 0, pos[1] - 1] = 1

    winners_mask = np.ones((21, 10), dtype=int)
    winners_mask = np.triu(winners_mask)

    total_winners = [0, 0]

    P = np.diag(np.ones(10, dtype=int))
    for _ in range(3):
        P = roll_quantum(P, axis=1)
    # P is [n_pos, n_pos]  =>  P[i, j] = "how many universes are created in pos j if one universe starts in pos j"

    player_turn = 0
    while (scores != 0).any():
        S = scores[player_turn]  # [n_scores, n_pos]  =>  S[i, j] = "how many universes are in pos j with score i"

        # Update S by playing a turn for the player
        S = S.reshape(21, 10, 1)  # Unsqueeze for broadcast
        S = S * P  # [n_scores, n_pos, n_pos]  =>  S[i, j, k] = "how many universes move from pos j to pos k with initial score i"
        S = S.sum(axis=1)  # [n_scores, n_pos]  => S[i, j] = "how many universes with initial score i are now in pos j"
        for col_idx, shift in enumerate(range(1, 11)):
            S[:, col_idx] = np.roll(S[:, col_idx], shift)  # Move universes to dedicated score

        total_winners[player_turn] += np.sum(S * winners_mask)  # Count ended games
        S = (1 - winners_mask) * S  # Remove ended games
        scores[player_turn] = S
        scores[1 - player_turn] *= 27  # Create 27 alternate universes with the same game state for each previous universe

        # TODO: remove ended games from other player
        # Use a matrix in [21 x 10 x 21 x 10] ?

        player_turn = 1 - player_turn

    return max(total_winners)


def main(path_input: str) -> int:
    pos = read_input(path_input)

    sol1 = determinist_dice(pos)

    sol2 = quantum_dice(pos)

    return sol1, sol2

if __name__ == '__main__':
    print('Solution for day 21')

    sol1, sol2 = main('example')
    print('Part 1:', sol1)
    print('Part 2:', sol2)
