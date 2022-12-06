#! /usr/bin/env python3
### stdlib imports
import re

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Split the puzzle input up into pairs of elves and their ranges
    elfAssignments: list[tuple[int, int, int, int]] = []
    for line in puzzleInput.strip().split("\n"):
        if match := re.match(r"^(\d+)-(\d+),(\d+)-(\d+)$", line):
            elfAssignments.append(tuple([int(n) for n in match.groups()]))

    # Tallies used for answers to parts 1 & 2
    partiallyContainedAssignments: int = 0
    fullyContainedAssignments: int = 0

    # Iterate through each elf pairing and figure out which sections have complete overlap
    for (
        section0Start,
        section0End,
        section1Start,
        section1End,
    ) in elfAssignments:
        # Create unique set based off the ranges
        range0 = set(range(section0Start, section0End + 1))
        range1 = set(range(section1Start, section1End + 1))
        overlap = len(range0.intersection(range1))

        # If there is partial overlap, increase the partial overlap tally
        if overlap > 0:
            partiallyContainedAssignments += 1

        # If the intersection of the two ranges is equal to the size of either one,
        # then that means one is completely contained and we should increase the tally
        if len(range0) == overlap or len(range1) == overlap:
            fullyContainedAssignments += 1

    # The answer to part 1 is the total number of fully contained assignments
    utils.printAnswer(fullyContainedAssignments)

    # Pass the answer for part 2 foward
    return partiallyContainedAssignments


@utils.part2
def part2(_, answer: int):
    utils.printAnswer(answer)


if __name__ == "__main__":
    utils.start()
