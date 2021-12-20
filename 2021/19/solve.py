from itertools import combinations, product

import numpy as np
from numpy.linalg import matrix_power


class Beacon:
    def __init__(self, x, y, z):
        self.coords = np.array([x, y, z])
        self.d_square = pow(self.coords, 2).sum()
        self.surroundings = list()
        self.absolute = None

    def dist_to(self, other) -> float:
        dist = pow(self.coords - other.coords, 2).sum()
        self.surroundings.append(dist)
        other.surroundings.append(dist)
        return dist

    def compare_surrondings(self, other) -> int:
        surroundings = other.surroundings.copy()
        for d in self.surroundings:
            if d in surroundings:
                surroundings.remove(d)

        return len(other.surroundings) - len(surroundings)

    def __repr__(self):
        return f'[{self.coords[0]}, {self.coords[1]}, {self.coords[2]}]'


class Scanner:
    def __init__(self, beacons: list, id: int):
        self.beacons = [Beacon(x, y, z) for x, y, z in beacons]
        self.position = np.zeros(3)
        self.id = id

    def compute_all_dists(self):
        for b1, b2 in combinations(self.beacons, 2):
            b1.dist_to(b2)

    def intersections(self, other) -> list:
        all_intersections = []
        for b1 in self.beacons:
            best_b, intersection = None, 0
            for b2 in other.beacons:
                inter = b1.compare_surrondings(b2)

                if inter > intersection:
                    intersection = inter
                    best_b = b2

            if intersection >= 11:
                all_intersections.append((b1, best_b, intersection))

        return all_intersections


    def __repr__(self):
        return f'Scanner {self.id}: {self.position}'


def find_pairs(scanners: list) -> list:
    pairs = []

    for s1, s2 in combinations(scanners, 2):
        intersections = s1.intersections(s2)
        if len(intersections) >= 12:
            pairs.append((s1, s2))

    return pairs


def eval_loss(source: np.array, beacons: np.array, distances: np.array) -> int:
    loss = pow(beacons - source, 2).sum(axis=1) - distances
    return abs(loss).sum()


def neighbours(cell: np.array):
    x, y, z = cell
    return [
        np.array([x+1, y, z]),
        np.array([x-1, y, z]),
        np.array([x, y+1, z]),
        np.array([x, y-1, z]),
        np.array([x, y, z+1]),
        np.array([x, y, z-1]),
        np.array([x+1, y+1, z]),
        np.array([x+1, y, z+1]),
        np.array([x, y+1, z+1]),
        np.array([x+1, y+1, z+1]),
        np.array([x-1, y-1, z]),
        np.array([x-1, y, z-1]),
        np.array([x, y-1, z-1]),
        np.array([x-1, y-1, z-1]),
        np.array([x-1, y+1, z]),
        np.array([x-1, y, z+1]),
        np.array([x, y-1, z+1]),
        np.array([x-1, y+1, z+1]),
        np.array([x+1, y-1, z]),
        np.array([x+1, y, z-1]),
        np.array([x, y+1, z-1]),
        np.array([x+1, y-1, z+1]),
        np.array([x+1, y+1, z-1]),
        np.array([x+1, y-1, z-1]),
        np.array([x-1, y-1, z+1]),
    ]


def find_source(beacons: np.array, distances: np.array) -> np.array:
    for source in beacons:
        current_loss = eval_loss(source, beacons, distances)
        has_moved = True
        while has_moved:
            has_moved = False

            for n in neighbours(source):
                loss = eval_loss(n, beacons, distances)
                if loss < current_loss:
                    has_moved = True
                    source = n
                    current_loss = loss

        if current_loss == 0:
            return source

    raise RuntimeError("Couldn't find the source!")


def check_transfo(transfo: np.array, interactions: list, origin: np.array) -> bool:
    for b1, b2, _ in interactions:
        ref = b1.absolute
        coords = transfo @ b2.coords + origin

        if (ref != coords).any():
            return False

    return True


def find_orient(interactions: list, origin: np.array) -> np.array:
    A = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])

    B = np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ])

    for a, b, c, d in product(range(4), range(4), range(4), range(4)):
        transfo = matrix_power(A, a) @ matrix_power(B, b) @ matrix_power(A, c) @ matrix_power(B, d)
        if check_transfo(transfo, interactions, origin):
            return transfo

    raise RuntimeError('No orientation found!')


def reorient(source: Scanner, other: Scanner):
    interactions = source.intersections(other)

    transfo = find_orient(interactions, other.position)

    for b in other.beacons:
        b.absolute = transfo @ b.coords + other.position


def repair_pair(source: Scanner, other: Scanner):
    intersections = source.intersections(other)

    beacons = np.array([
        b.absolute
        for b, _, _ in intersections
    ])

    distances = np.array([
        b.d_square
        for _, b, _ in intersections
    ])

    position = find_source(beacons, distances)
    other.position = position

    reorient(source, other)


def repair_all_pairs(pairs: list):
    source, other = pairs.pop(0)
    for b in source.beacons:
        b.absolute = b.coords

    repair_pair(source, other)

    repaired = [source, other]
    while pairs:
        to_remove = []
        for s1, s2 in pairs:
            if s1 in repaired or s2 in repaired:
                if s1 not in repaired:
                    repair_pair(s2, s1)
                    repaired.append(s1)
                elif s2 not in repaired:
                    repair_pair(s1, s2)
                    repaired.append(s2)

                to_remove.append((s1, s2))

        for pair in to_remove:
            pairs.remove(pair)


def parse_input(lines: list):
    scanners = []
    current_scanner = []
    for line in lines:
        line = line.replace('\n', '')

        if line == '':
            scanners.append(current_scanner)
            continue

        if line.startswith('---'):
            current_scanner = []
            continue

        numbers = [int(n) for n in line.split(',')]
        current_scanner.append(numbers)

    # Append last scanner
    scanners.append(current_scanner)
    scanners = [Scanner(beacons, id) for id, beacons in enumerate(scanners)]
    return scanners


def solve(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    scanners = parse_input(lines)
    for s in scanners:
        s.compute_all_dists()

    pairs = find_pairs(scanners)
    repair_all_pairs(pairs)

    unique_beacon = set()
    for s in scanners:
        for b in s.beacons:
            unique_beacon.add(tuple(b.absolute))

    sol1 = len(unique_beacon)

    sol2 = 0
    for s1, s2 in combinations(scanners, 2):
        dist = s1.position - s2.position
        dist = abs(dist).sum()

        sol2 = max(sol2, dist)

    return sol1, sol2


if __name__ == '__main__':
    print('Solution for day 10')

    sol1, sol2 = solve('input')
    print('Part 1:', sol1)
    print('Part 2:', sol2)
