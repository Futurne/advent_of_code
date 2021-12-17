"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.
Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.
How many dots are visible after completing just the first fold instruction on your transparent paper?

--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.
What code do you use to activate the infrared thermal imaging camera system?
"""
import numpy as np
from pipe import select, where


def lines_to_matrix(lines: list[str]) -> np.array:
    data = list(lines
        | where(lambda l: ',' in l)
        | select(lambda l: l.replace('\n', ''))
        | select(lambda l: l.split(','))
        | select(lambda values: (int(values[0]), int(values[1])))
    )
    max_x = max(v[0] for v in data)
    max_y = max(v[1] for v in data)

    matrix = np.zeros((max_x+1, max_y+1), dtype=bool)

    for cell in data:
        matrix[cell] = True

    return matrix


def parse_folds(lines: list[str]) -> list[tuple]:
    folds = list(lines
        | where(lambda l: 'fold' in l)
        | select(lambda l: l[len('fold along '):])
        | select(lambda l: l.split('='))
        | select(lambda values: (values[0], int(values[1])))
    )
    return folds


def fold_along(matrix: np.array, axis: str, axis_value: int) -> np.array:
    if axis == 'x':
        m1, m2 = matrix[:axis_value], matrix[axis_value+1:][::-1]
        pad = np.zeros((m1.shape[0] - m2.shape[0], m1.shape[1]), dtype=bool)
        m2 = np.concatenate([pad, m2], axis=0)
    else:
        m1, m2 = matrix[:, :axis_value], matrix[:, axis_value+1:][:, ::-1]
        pad = np.zeros((m1.shape[0], m1.shape[1] - m2.shape[1]), dtype=bool)
        m2 = np.concatenate([pad, m2], axis=1)

    return m1 + m2


def solve(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    matrix = lines_to_matrix(lines)
    folds = parse_folds(lines)
    f = folds[0]
    return fold_along(matrix, f[0], f[1]).sum()


def solve_2(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    matrix = lines_to_matrix(lines)
    folds = parse_folds(lines)
    for (axis, axis_value) in folds:
        matrix = fold_along(matrix, axis, axis_value)

    return matrix.T

if __name__ == '__main__':
    print('Solution for day 12')

    solution = solve('input')
    print('Part 1:', solution)

    solution = solve_2('input')
    print('Part 2:')
    for row in solution:
        for el in row:
            print('#' if el else '.', end='')
        print('')
