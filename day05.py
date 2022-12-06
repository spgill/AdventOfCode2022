#! /usr/bin/env python3
### stdlib imports
import copy
import re

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Take the input and split the create arrangement apart from the instructions
    cratesRaw, instructionsRaw = puzzleInput.rstrip().split("\n\n")

    # Parse the crate input into usable data structures
    crateStacksRaw = cratesRaw.split("\n")[:-1]
    stackCount = (len(crateStacksRaw[0]) + 1) // 4
    crateStacks: list[list[str]] = [list() for i in range(stackCount)]
    for stackRow in crateStacksRaw:
        for i, match in enumerate(
            re.finditer(r"(?:   |\[(\w)\])(?:[ \n]|$)", stackRow)
        ):
            character = match.group(1)
            if not character:
                continue
            crateStacks[i].insert(0, character)

    # Create a copy for reuse later
    clone = copy.deepcopy(crateStacks)

    # Parse the instructions into a list of arguments
    instructions: list[tuple[int, int, int]] = []
    for line in instructionsRaw.split("\n"):
        if match := re.match(r"^move (\d+) from (\d+) to (\d+)$", line):
            instructions.append(tuple([int(n) for n in match.groups()]))

    # Iterate through each instruction and execute the crane maneuvers
    for quantity, source, destination in instructions:
        # Align the instructions with our 0-indexed list
        source -= 1
        destination -= 1

        # Grab however many crates specified, and insert them into the destination stack
        grabbed = [crateStacks[source].pop() for _ in range(quantity)]
        [crateStacks[destination].append(c) for c in grabbed]

    # The answer is derived by concatenating all of the top crates
    utils.printAnswer("".join([stack.pop() for stack in crateStacks]))

    # Pass clone of the stacks and the instructions to part 2
    return (clone, instructions)


@utils.part2
def part2(_, part1Data: tuple[list[list[str]], list[tuple[int, int, int]]]):
    crateStacks, instructions = part1Data

    # Perform a similar iteration to part 1, only this time we're going to be moving multiple crates at once
    for quantity, source, destination in instructions:
        # Align the instructions with our 0-indexed list
        source -= 1
        destination -= 1

        # Grab however many crates specified, and insert them into the destination stack
        # We reverse them on insertion to maintain the original order as prescribed by part 2
        grabbed = [crateStacks[source].pop() for _ in range(quantity)]
        [crateStacks[destination].append(c) for c in reversed(grabbed)]

    # The answer is derived the same way as part 1
    utils.printAnswer("".join([stack.pop() for stack in crateStacks]))


if __name__ == "__main__":
    utils.start()
