#! /usr/bin/env python3
### stdlib imports
import typing

### vendor imports
import advent_of_code_ocr
import numpy

### local imports
import utils


def generatePipeline(
    instructions: list[tuple[str, int]]
) -> typing.Generator[int, None, None]:
    """Generate a sequence of integer instructions from a list of puzzle instructions."""
    for command, value in instructions:
        if command == "noop":
            yield 0
        elif command == "addx":
            yield 0
            yield value


@utils.part1
def part1(puzzleInput: str):
    # Split the input into a list of instructions
    instructions: list[tuple[str, int]] = [
        (line.split()[0], int((line + " 0").split()[1]))
        for line in puzzleInput.strip().split("\n")
    ]

    # Iterate through list of desired samples and simulate them from the execution pipeline
    samples = [20, 60, 100, 140, 180, 220]
    pipeline = list(generatePipeline(instructions))
    utils.printAnswer(sum((sum(pipeline[: n - 1]) + 1) * n for n in samples))

    # Pass the instructions to part 2
    return instructions


litPixel = "#"
darkPixel = "."


@utils.part2
def part2(_, instructions: list[tuple[str, int]]):
    # For part 2, we will be simulating the program rendering to a CRT screen... or something like that

    register: int = 1
    completeLines: list[str] = []
    currentLine = ""
    wrapPoints = [40, 80, 120, 160, 200, 240]

    # Iterate through each execution cycle and render the CRT lines
    for i, addend in enumerate(generatePipeline(instructions)):
        cycle = i + 1
        cursorPosition = i % 40

        # If register is out of range, ignore this cycle
        centerPixel = register
        if 0 > centerPixel > 39:
            currentLine += darkPixel

        else:
            # Calculate the three pixel window from the register value
            windowStart = numpy.clip(centerPixel - 1, 0, 39)
            windowEnd = numpy.clip(centerPixel + 1, 0, 39)
            window = list(range(windowStart, windowEnd + 1))

            # If the cursor lies within the current window, add a lit pixel
            if cursorPosition in window:
                currentLine += litPixel
            else:
                currentLine += darkPixel

        # Update the register with the current addend
        register += addend

        # If this was the last cycle of a wrap, append the current line and start a new one
        if cycle in wrapPoints:
            completeLines.append(currentLine)
            currentLine = ""

    # Use the AoC OCR library to convert the lines to characters
    utils.printAnswer(advent_of_code_ocr.convert_6("\n".join(completeLines)))


if __name__ == "__main__":
    utils.start()
