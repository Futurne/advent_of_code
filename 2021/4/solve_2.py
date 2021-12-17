"""--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant squid win.
You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.
In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.
Figure out which board will win last. Once it wins, what would its final score be?
"""
import numpy as np


class Board:
    def __init__(self, board: np.array):
        self.board = board
        self.bool_board = np.zeros(board.shape, dtype=bool)
        self.coords = {
            el: (x, y)
            for x, row in enumerate(board)
            for y, el in enumerate(row)
        }

    def draw(self, number: int) -> bool:
        """If the number is in the board,
        it marks it.
        Tells whether or not the board has won.
        """
        if number not in self.coords:
            return False

        coords = self.coords[number]
        self.bool_board[coords] = True
        return self.bool_board[coords[0], :].all() or self.bool_board[:, coords[1]].all()


def drawn_numbers(line_generator) -> list[int]:
    numbers = next(line_generator).replace('\n', '')
    numbers = [int(n) for n in numbers.split(',')]
    next(line_generator)  # Empty line
    return numbers


def read_boards(line_generator) -> list[np.array]:
    boards = []
    board = []
    for line in line_generator:
        line = line.replace('\n', '')
        if line == '':
            boards.append(np.array(board))
            board = []
        else:
            board.append([int(n) for n in line.split(' ')
                if n != ''])

    boards.append(np.array(board))
    return boards


def score(board, n):
    return ((~board.bool_board) * board.board).sum() * n


def solve(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        line_generator = iter(input_file)
        numbers = drawn_numbers(line_generator)
        boards = read_boards(line_generator)

    boards = [Board(b) for b in boards]
    winners = [False for _ in boards]
    for n in numbers:
        for board_id, board in enumerate(boards):
            if board.draw(n):
                winners[board_id] = True

                if all(winners):
                    return score(board, n)


if __name__ == '__main__':
    solution = solve('input')
    print('Solution for day 4 part 2:', solution)
