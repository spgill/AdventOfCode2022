#! /usr/bin/env python3
### stdlib imports
import math
import typing

### local imports
import utils


CoordGrid = list[list[str]]
Coord = tuple[int, int]
CoordPath = list[tuple[int, int]]


def getGridSize(grid: CoordGrid) -> tuple[int, int]:
    return (len(grid[0]), len(grid))


def findPoint(grid: CoordGrid, char: str) -> Coord:
    for y, row in enumerate(grid):
        for x, rowChar in enumerate(row):
            if rowChar == char:
                return (x, y)

    utils.printError(f"Char '{char}' not found in grid")
    exit(1)


def getNeighbors(
    grid: CoordGrid, point: Coord
) -> typing.Generator[Coord, None, None]:
    pointX, pointY = point
    pointLevel = ord(grid[pointY][pointX])
    limitX, limitY = getGridSize(grid)
    for modX, modY in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        x = pointX + modX
        y = pointY + modY
        if (
            -1 < x < limitX
            and -1 < y < limitY
            and ord(grid[y][x]) >= (pointLevel - 1)
        ):
            yield (x, y)


def createTraveralDistanceMap(
    grid: CoordGrid, point: Coord
) -> dict[Coord, int]:
    """Using the BFS grid traversal technique, create a mapping of start points to their traversal distance."""
    queue: CoordPath = [point]
    distanceMap: dict[Coord, int] = {}
    distanceMap[point] = 0

    while queue:
        current = queue.pop(0)
        for neighbor in getNeighbors(grid, current):
            if neighbor not in distanceMap:
                distanceMap[neighbor] = distanceMap[current] + 1
                queue.append(neighbor)

    return distanceMap


@utils.part1
def part1(puzzleInput: str):
    # Split the puzzle input into an addressable grid
    grid: CoordGrid = [list(row) for row in puzzleInput.strip().split("\n")]

    # Find the origin coordinates
    origin = findPoint(grid, "S")
    destination = findPoint(grid, "E")

    # Modify the origin and destination points with the current character representing their heights
    originX, originY = origin
    destX, destY = destination
    grid[originY][originX] = "a"
    grid[destY][destX] = "z"

    # Starting from the end point, create a mapping of traversal distances
    traversalMap = createTraveralDistanceMap(grid, destination)

    # The answer is the traversal distance to the origin point
    utils.printAnswer(traversalMap[origin])

    # Return the grid and traversal map for part 2 to work with
    return (grid, traversalMap)


@utils.part2
def part2(_, part1Data: tuple[CoordGrid, dict[Coord, int]]):
    grid, traversalMap = part1Data

    # Find all points on the map with the same elevation as the origin
    candidates: list[Coord] = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "a":
                candidates.append((x, y))

    # The answer is the candidate with the shortest path to the destination point
    utils.printAnswer(min([traversalMap.get(c, math.inf) for c in candidates]))


if __name__ == "__main__":
    utils.start()
