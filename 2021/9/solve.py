"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.
If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).
Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.
Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)
In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.
The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.
Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?


--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.
A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.
The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.
What do you get if you multiply together the sizes of the three largest basins?
"""
import numpy as np


def to_matrix(lines: list[str]) -> np.array:
    lines = [l.replace('\n', '') for l in lines]
    matrix = [
        [int(n) for n in l]
        for l in lines
    ]
    return np.array(matrix)


def discrete_gradient(matrix: np.array) -> np.array:
    """Discrete derivative of all the directions.
    Everytime we derive of a side, we pad a serie of '1' to this side.
    """
    d_right = matrix[:, :-1] - matrix[:, 1:]
    pad = np.ones((d_right.shape[0], 1))
    d_right = np.concatenate([pad, d_right], axis=1)

    d_left = matrix[:, 1:] - matrix[:, :-1]
    pad = np.ones((d_left.shape[0], 1))
    d_left = np.concatenate([d_left, pad], axis=1)

    d_up = matrix[:-1] - matrix[1:]
    pad = np.ones((1, d_up.shape[1]))
    d_up = np.concatenate([pad, d_up], axis=0)

    d_low = matrix[1:] - matrix[:-1]
    pad = np.ones((1, d_low.shape[1]))
    d_low = np.concatenate([d_low, pad], axis=0)

    return d_right, d_left, d_up, d_low


def low_points(gradients: list[np.array]) -> np.array:
    """Mask of all the low points.
    A low point is a point where all gradients are > 0.
    """
    mask = np.ones(gradients[0].shape, dtype=bool)
    for g in gradients:
        mask *= (g > 0)
    return mask


def solve(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    matrix = to_matrix(lines)
    gradients = discrete_gradient(matrix)
    mask = low_points(gradients)
    points = (mask * matrix).sum()
    return points + mask.sum()  # Add '1' to each low points


def find_neighbours(cell: tuple, available_cells: set[tuple]) -> list[tuple]:
    """Find all neighbours in the `available_cells`.

    Return those neighbours.
    """
    neighbours = [cell]
    to_visit = [cell]  # LIFO

    while to_visit:
        x, y = to_visit.pop()

        for n in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if n in available_cells:
                neighbours.append(n)
                to_visit.append(n)
                available_cells.remove(n)

    return neighbours


def connectivity(matrix: np.array) -> list[set]:
    """Find all group of cells that are freely walkable
    by the player.

    Return a list of set of cells. Each set contains
    the cells that can be reach by each other.
    """
    # Transforms the numpy array into a set of tuples
    available_cells = np.argwhere(matrix != 9).tolist()
    available_cells = set(tuple(c) for c in available_cells)
    neighbours = []

    while available_cells:
        current_cell = available_cells.pop()
        n = find_neighbours(current_cell, available_cells)
        neighbours.append(set(n))

    return neighbours


def solve_2(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    matrix = to_matrix(lines)
    neightbours = connectivity(matrix)
    sizes = [len(n) for n in neightbours]
    sizes = list(sorted(sizes))[-3:]
    return sizes[0] * sizes[1] * sizes[2]


if __name__ == '__main__':
    print('Solution for day 9')

    solution = solve('input')
    print('Part 1:', solution)

    solution = solve_2('input')
    print('Part 2:', solution)
