#! /usr/bin/env python3
### vendor imports
import more_itertools

### local imports
import utils


def findUniqueCharactersEndpoint(datastream: str, length: int):
    # Iterate through the datastream in a moving window of size `length`
    for i, block in enumerate(more_itertools.windowed(datastream, length)):
        # If the length of the unique character set is the same as the block,
        # then all characters are unique
        unique = set(block)
        if len(block) == len(unique):
            # Add the length, because we are returning the _endpoint_
            return i + length


@utils.part1
def part1(puzzleInput: str):
    datastream = puzzleInput.strip()

    # Find unique characters in a 4 character window
    utils.printAnswer(findUniqueCharactersEndpoint(datastream, 4))

    # Return the datastream for part 2 to work with
    return datastream


@utils.part2
def part2(_, datastream: str):
    # The answer is found the same as before, only the window size is larger
    utils.printAnswer(findUniqueCharactersEndpoint(datastream, 14))


if __name__ == "__main__":
    utils.start()
