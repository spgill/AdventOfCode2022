#! /usr/bin/env python3

### local imports
import utils

# Losing moves (+0 modifier)
losingMoves: dict[str, int] = {
    "A Z": 3 + 0,  # rock v scissors
    "B X": 1 + 0,  # paper v rock
    "C Y": 2 + 0,  # scissors v paper
}

# Draw moves (+3 modifier)
drawMoves: dict[str, int] = {
    "A X": 1 + 3,  # rock v rock
    "B Y": 2 + 3,  # paper v paper
    "C Z": 3 + 3,  # scissors v scissors
}

# Winning moves (+6 modifier)
winningMoves: dict[str, int] = {
    "A Y": 2 + 6,  # , rock v paper
    "B Z": 3 + 6,  # paper v scissors
    "C X": 1 + 6,  # scissors v rock
}

# Mapping of ALL the possible move combinations
allMoves: dict[str, int] = {**losingMoves, **drawMoves, **winningMoves}


@utils.part1
def part1(puzzleInput: str):
    # Break the puzzle input down into a list of moves
    moves = puzzleInput.strip().split("\n")

    # Calculate the final score from the sum of point values of all moves in the list
    utils.printAnswer(sum([allMoves[move] for move in moves]))

    # Return the moves list for part 2 to work with
    return moves


@utils.part2
def part2(_, moves: list[str]):
    finalScore: int = 0

    # Iterate through each move in the list
    for opponentMove, outcome in [move.split(" ") for move in moves]:
        # Select the list of possible moves based on the ordained outcome
        possibleMoves = {"X": losingMoves, "Y": drawMoves, "Z": winningMoves}[
            outcome
        ]

        # Iterate through the possible moves to find one that matches the opponent's move.
        # When it matches, add the point value and move on
        for move, moveValue in possibleMoves.items():
            if move.startswith(opponentMove):
                finalScore += moveValue
                break

    # The answer is the final score
    utils.printAnswer(finalScore)


if __name__ == "__main__":
    utils.start()
