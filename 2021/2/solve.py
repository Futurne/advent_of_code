"""--- Day 2: Dive! ---

Now, you need to figure out how to pilot this thing.
It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.

Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.
The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2

Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""
import re

from pipe import Pipe, select, where


@Pipe
def select_forward(iterable):
    pattern = 'forward (?P<number>\d+)\n?'
    pattern = re.compile(pattern)

    for command in iterable:
        value = pattern.sub(r'\g<number>', command)
        yield int(value)


@Pipe
def select_depth(iterable):
    pattern_up = r'up (?P<number>\d+)\n?'
    pattern_up = re.compile(pattern_up)
    pattern_down = r'down (?P<number>\d+)\n?'
    pattern_down = re.compile(pattern_down)

    for command in iterable:
        value = pattern_up.sub(r'-\g<number>', command)
        value = pattern_down.sub(r'\g<number>', value)
        yield int(value)


@Pipe
def where_forward(iterable):
    pattern = 'forward \d+\n?'
    pattern = re.compile(pattern)
    for command in iterable:
        if pattern.match(command):
            yield command


@Pipe
def where_depth(iterable):
    pattern = '(up|down) \d\n?'
    pattern = re.compile(pattern)
    for command in iterable:
        if pattern.match(command):
            yield command


def solve(input_path: str) -> int:
    with open(input_path, 'r') as input_file:
        count_forward = sum(input_file | where_forward
                | select_forward)

    with open(input_path, 'r') as input_file:
        count_depth = sum(input_file | where_depth
                | select_depth)

    return count_forward * count_depth


if __name__ == '__main__':
    solution = solve('input')
    print('Solution of day 2:', solution)
