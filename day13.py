#! /usr/bin/env python3
### stdlib imports
import functools
import itertools
import math
import typing

### vendor imports
import more_itertools

### local imports
import utils


Packet = list[typing.Union["Packet", int]]

# The divider packets specified by part 2
dividerPackets: list[Packet] = [[[2]], [[6]]]


def sortPackets(
    left: typing.Union[Packet, int],
    right: typing.Union[Packet, int],
) -> int:
    # If they are both integers, they can be compared directly
    if isinstance(left, int) and isinstance(right, int):
        # If left is less than right, they are sorted correctly
        if left < right:
            return 1

        # If left is greater than right, they are NOT sorted correctly
        elif left > right:
            return -1

    # Else one of the sides is a list, and we must iterate through
    else:
        # Convert whichever side is a bare int to a list
        left = [left] if isinstance(left, int) else left
        right = [right] if isinstance(right, int) else right

        # Iterate through the members of both, filling in None for missing values (i.e., mismatched list sizes)
        for i, j in itertools.zip_longest(left, right, fillvalue=None):
            # If left side runs out, these packets are sorted correctly
            if i is None:
                return 1

            # If right side runs out, these packets are NOT sorted correctly
            if j is None:
                return -1

            # Compare the nested values and return if they come to a conclusion
            if (result := sortPackets(i, j)) != 0:
                return result

    # If a verdict has not been made, return None
    return 0


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input into pairs of packets
    packetPairs: list[tuple[Packet, Packet]] = [
        (eval(pair.split("\n")[0]), eval(pair.split("\n")[1]))
        for pair in puzzleInput.strip().split("\n\n")
    ]

    # The answer is the sum of indices of all packets pairs that are correctly sorted
    utils.printAnswer(
        sum(
            n + 1
            for n, pair in enumerate(packetPairs)
            if sortPackets(*pair) > 0
        )
    )

    # Return the packet pairs for part
    return packetPairs


@utils.part2
def part2(_, packetPairs: list[tuple[Packet, Packet]]):

    # Flatten the packet pairs and include the two divider packets
    packets = list(more_itertools.flatten(packetPairs)) + dividerPackets

    # Sort the packets using our method created for part 1
    packets.sort(key=functools.cmp_to_key(sortPackets), reverse=True)

    # Find the indexes of the divider packets, and the product is our answer
    utils.printAnswer(math.prod(packets.index(d) + 1 for d in dividerPackets))


if __name__ == "__main__":
    utils.start()
