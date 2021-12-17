"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.
Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)
Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?


--- Part Two ---

After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""
class Path:
    def __init__(self):
        self.path = []
        self.small_cave_visited_twice = False

    def copy(self):
        p_cpy = Path()
        p_cpy.path = self.path.copy()
        p_cpy.small_cave_visited_twice = self.small_cave_visited_twice
        return p_cpy

    def append(self, node):
        if node.is_small and node in self.path:
            assert not self.small_cave_visited_twice
            self.small_cave_visited_twice = True
        self.path.append(node)


class Node:
    def __init__(self, node_id: str):
        self.id = node_id
        self.is_small = self.id.islower()
        self.links = []

    def find_paths(self, path: Path, allow_twice: bool) -> list:
        path.append(self)

        if self.id == 'end':
            return [path]

        paths = []
        for node in self.links:
            if node.id == 'start':
                continue  # Don't come back to the starting node

            if node.is_small and node in path.path:
                # Small cave already in path
                if not allow_twice or path.small_cave_visited_twice:
                    # Either we don't allow two visits to a single small cave or we already did it
                    continue

            p = path.copy()
            paths.extend(node.find_paths(p, allow_twice))

        return paths

    def __eq__(self, other):
        return self.id == other.id


class Tree:
    def __init__(self, lines: list[str]):
        self.start = None
        self.nodes = dict()

        self.build_tree(lines)

    def build_tree(self, lines: list[str]):
        lines = [l.replace('\n', '') for l in lines]
        for l in lines:
            l = l.split('-')
            id1, id2 = l[0], l[1]

            node1 = self.nodes[id1] if id1 in self.nodes else Node(id1)
            node2 = self.nodes[id2] if id2 in self.nodes else Node(id2)

            node1.links.append(node2)
            node2.links.append(node1)

            self.nodes[id1] = node1
            self.nodes[id2] = node2

        self.start = self.nodes['start']

    def find_paths(self, allow_twice: bool):
        paths = self.start.find_paths(Path(), allow_twice)
        return paths


def solve(input_path: str, allow_twice: bool) -> int:
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    tree = Tree(lines)
    return len(tree.find_paths(allow_twice))


if __name__ == '__main__':
    print('Solution for day 12')

    solution = solve('input', allow_twice=False)
    print('Part 1:', solution)

    solution = solve('input', allow_twice=True)
    print('Part 2:', solution)
