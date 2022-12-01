#! /usr/bin/env python3

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Split the input up into groups
    calorieGroups = puzzleInput.strip().split("\n\n")

    # Summate all calories within a group
    calorieSums = [
        sum([int(calorie) for calorie in group.strip().split("\n")])
        for group in calorieGroups
    ]

    # The answer is the largest sum
    utils.printAnswer(max(calorieSums))

    # Return the sums for part 2 to use
    return calorieSums


@utils.part2
def part2(_, calorieSums: list[int]):
    # The answer is the sum of the three largest calorie sums
    utils.printAnswer(sum(sorted(calorieSums, reverse=True)[:3]))


if __name__ == "__main__":
    utils.start()
