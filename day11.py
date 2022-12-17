#! /usr/bin/env python3
### stdlib imports
import copy
import dataclasses
import math
import re

### local imports
import utils


@dataclasses.dataclass(unsafe_hash=True)
class Monkey:
    id: int
    items: list[int]
    operation: str
    testDivisor: int
    testTargets: dict[bool, int]
    inspectionCount: int = 0


def simulateMonkeyBusiness(
    originalMonkeyList: list[Monkey], rounds: int, boredMonkeys: bool
) -> int:
    # Make a copy of the monkey list so we don't mutate the original
    monkeyList = copy.deepcopy(originalMonkeyList)

    commonPower = math.prod(monkey.testDivisor for monkey in monkeyList)

    # Iterate through the desired number of rounds of monkey business
    for _ in range(rounds):
        # In a single round, every monkey gets a turn, in order
        for monkey in monkeyList:
            # Iterate through the items to inspect this round
            for item in monkey.items:
                # Evaltuate the complete worry level for this item
                item = eval(monkey.operation, {"old": item})

                # If monkeys get bored in this simulation, divide by 3
                if boredMonkeys:
                    item //= 3

                # Else, modulo by a common power. Else, the numbers will grow exponentially
                else:
                    item = item % commonPower

                # Test if the item worry level is properly divisible
                testResult = (item % monkey.testDivisor) == 0

                # Toss this new item to the correct monkey based on the test results
                monkeyList[monkey.testTargets[testResult]].items.append(item)

                # Increase the monkey's inspection count
                monkey.inspectionCount += 1

            # Clear this monkey's item list
            del monkey.items
            monkey.items = []

    # Return the product of the number of items that the two most productive monkeys inspected over all the rounds
    return math.prod(
        sorted([monkey.inspectionCount for monkey in monkeyList])[-2:]
    )


@utils.part1
def part1(puzzleInput: str):
    monkeyList: list[Monkey] = []

    # Parse the puzzle input into a list of monkey objects
    for monkeyDefinitionText in puzzleInput.strip().split("\n\n"):
        if match := re.search(
            r"Monkey (\d+):\W+Starting items: (.*)\W+Operation:.*= (.*)\W+Test:\D*(\d+)\W+.*true:\D+(\d+)\W+.*false:\D+(\d+)",
            monkeyDefinitionText.strip(),
        ):
            groups = match.groups()
            monkeyList.append(
                Monkey(
                    id=int(groups[0]),
                    items=[int(n) for n in groups[1].split(", ")],
                    operation=groups[2],
                    testDivisor=int(groups[3]),
                    testTargets={
                        True: int(groups[4]),
                        False: int(groups[5]),
                    },
                )
            )
        else:
            utils.printError(
                "Error parsing monkey definition in puzzle input:"
            )
            utils.printMessage(monkeyDefinitionText)
            exit(1)

    # Make sure the list of monkeys are sorted correctly
    monkeyList.sort(key=lambda m: m.id)

    # The answer comes from simulating this monkeys doing their monkey business for 20 rounds
    utils.printAnswer(simulateMonkeyBusiness(monkeyList, 20, True))

    # Return the monkey list for part 2
    return monkeyList


@utils.part2
def part2(_, monkeyList: list[Monkey]):
    # The answer for part 2 comes from simulating the same monkey business for 10,000 rounds,
    # without accounting for monkey boredom.
    utils.printAnswer(simulateMonkeyBusiness(monkeyList, 10000, False))


if __name__ == "__main__":
    utils.start()
