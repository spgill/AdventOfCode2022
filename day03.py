#! /usr/bin/env python3
### vendor imports
import more_itertools

### local imports
import utils


priorityList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


@utils.part1
def part1(puzzleInput: str):
    # Split the input up into rucksacks
    rucksacks = puzzleInput.strip().split("\n")

    prioritySum: int = 0

    # Iterate through the two compartments of each sack
    for firstCompartment, secondCompartment in [
        (sack[: int(len(sack) / 2)], sack[int(len(sack) / 2) :])
        for sack in rucksacks
    ]:
        # Find the overlapping items between the two compartments
        commonItems = set(firstCompartment).intersection(
            set(secondCompartment)
        )

        # For each common item (should only be one), add it to the priority sum
        for item in commonItems:
            prioritySum += priorityList.index(item) + 1

    # The answer is the sum of all common compartment item priorities
    utils.printAnswer(prioritySum)

    # Pass rucksack list to part two
    return rucksacks


@utils.part2
def part2(_, rucksacks: list[str]):
    prioritySum: int = 0

    # Iterate through each group of three rucksacks
    for rucksack0, rucksack1, rucksack2 in more_itertools.chunked(
        rucksacks, 3
    ):
        # Find the overlapping items between the two compartments
        commonItems = (
            set(rucksack0)
            .intersection(set(rucksack1))
            .intersection(set(rucksack2))
        )

        # For each common item (should only be one), add it to the priority sum
        for item in commonItems:
            prioritySum += priorityList.index(item) + 1

    # The answer is the sum of all common group item priorities
    utils.printAnswer(prioritySum)


if __name__ == "__main__":
    utils.start()
