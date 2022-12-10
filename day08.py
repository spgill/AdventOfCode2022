#! /usr/bin/env python3
### stdlib imports
from functools import reduce

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Format the input as a grid of ints
    grid: list[list[int]] = []
    for line in puzzleInput.strip().split("\n"):
        grid.append([int(x) for x in line])

    visible = 0
    scenicScores: list[int] = []

    # Iterate through the inner square of the grid
    yStart = 1
    yEnd = len(grid)
    xStart = 1
    xEnd = len(grid[0])
    for y in range(yStart, yEnd - 1):
        for x in range(xStart, xEnd - 1):
            tree = grid[y][x]

            # Extract the row and column that the tree sits on
            row = grid[y].copy()
            column = [row.copy().pop(x) for i, row in enumerate(grid)]

            left = list(reversed(row[:x]))
            right = row[x + 1 :]

            above = list(reversed(column[:y]))
            below = column[y + 1 :]

            # If the tree is higher than the highest tree in any direction, it is visible
            if (
                tree > max(left)
                or tree > max(right)
                or tree > max(above)
                or tree > max(below)
            ):
                visible += 1

            # While we're iterating through the grid, calculate the scenic scores for part 2
            sightLines = [above, left, below, right]
            scenicComponents: list[int] = []
            for line in sightLines:
                component = 0
                for n in line:
                    if n >= tree:
                        component += 1
                        break
                    else:
                        component += 1
                scenicComponents.append(component)
            scenicScores.append(reduce(lambda x, y: x * y, scenicComponents))

    # The answer is the count of visible trees, including the surrounding ones
    utils.printAnswer(visible + (yEnd * 2) + ((xEnd - 2) * 2))

    # The answer to part 2 is the highest scenic score. Pass it to part 2 to print out.
    return max(scenicScores)


@utils.part2
def part2(_, highestScenicScore: int):
    utils.printAnswer(highestScenicScore)


if __name__ == "__main__":
    utils.start()
