#! /usr/bin/env python3
### vendor imports
import numpy
import numpy.linalg

### local imports
import utils


movementVectors: dict[str, tuple[int, int]] = {
    "U": (0, 1),
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


def simulateRope(instructions: list[tuple[str, int]], length: int) -> int:
    """Simulate movement of a rope of size `length` in a grid.

    Arguments:
        instructions: list of instructions for movement of the rope head.
        length: length of the rope NOT including the head.
    """
    # Create a list of tuples to track the positions of rope segments
    ropeSegments: list[tuple[int, int]] = [(0, 0) for i in range(length + 1)]

    # This set is to track the unique positions that the tail of the rope has visited
    tailLocations: set[tuple[int, int]] = set()

    # Iterate through the instructions and move the rope segments around accordingly
    for direction, directionMagnitude in instructions:
        directionVector = movementVectors[direction]
        for i in range(directionMagnitude):
            for j, segment in enumerate(ropeSegments):
                # If this is the head segment, move it in the direction given by the instruction
                if j == 0:
                    segment = tuple(numpy.add(segment, directionVector))

                # Else, we move the segment towards the previous segment
                else:
                    target = ropeSegments[j - 1]

                    # Calculate the difference between the segment and target locations
                    distance = tuple(numpy.subtract(target, segment))
                    distanceMagnitude = numpy.linalg.norm(distance)

                    # If the magnitude of the distance is at least 2, we move the tail towards the head
                    if distanceMagnitude >= 2.0:
                        clippedDistance = tuple(
                            numpy.clip(distance, (-1, -1), (1, 1))
                        )
                        segment = tuple(numpy.add(segment, clippedDistance))

                # Update the segment location in the array
                ropeSegments[j] = segment

            # Add the tail's location to the set
            tailLocations.add(ropeSegments[-1])

    # Return the length of unique locations the tail visited
    return len(tailLocations)


@utils.part1
def part1(puzzleInput: str):
    # Split the puzzle input into a list of instructions
    instructions: list[tuple[str, int]] = [
        (line.split()[0], int(line.split()[1]))
        for line in puzzleInput.strip().split("\n")
    ]

    # Simulate the rope with a length of 1
    utils.printAnswer(simulateRope(instructions, 1))

    # Return the instructions list for part 2 to utilize
    return instructions


@utils.part2
def part2(_, instructions: list[tuple[str, int]]):
    # Simulate the rope with a length of 9 this time
    utils.printAnswer(simulateRope(instructions, 9))


if __name__ == "__main__":
    utils.start()
