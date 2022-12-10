#! /usr/bin/env python3
### stdlib imports
from dataclasses import dataclass
import typing

### local imports
import utils


@dataclass
class FilePointer:
    name: str
    size: int


@dataclass
class DirectoryPointer:
    name: str
    parent: typing.Optional["DirectoryPointer"]
    children: list["DirectoryPointer"]
    files: list[FilePointer]

    def getPathString(self) -> str:
        lineage: list[DirectoryPointer] = []
        parent = self
        while parent is not None:
            lineage.append(parent)
            parent = parent.parent
        return "/".join(reversed([member.name for member in lineage]))

    def __repr__(self) -> str:
        return f"DirectoryPointer({self.getPathString()})"

    def __hash__(self) -> int:
        return hash(self.getPathString())

    def getTotalSize(self) -> int:
        # Sum the size of files belonging to this directory
        fileSum = sum([file.size for file in self.files])

        # Sum the size of all child directories
        childSum = sum([child.getTotalSize() for child in self.children])

        # Return the.... wait for it.... sum :)
        return fileSum + childSum

    def _populateAllDirectories(
        self, directorySet: set["DirectoryPointer"]
    ) -> None:
        directorySet.add(self)
        for child in self.children:
            child._populateAllDirectories(directorySet)

    def getAllDirectories(self) -> list["DirectoryPointer"]:
        directorySet: set[DirectoryPointer] = set()
        self._populateAllDirectories(directorySet)
        return list(directorySet)


def createDirectoryStructure(instructions: list[str]) -> DirectoryPointer:
    # Create the root directory to begin the structure
    rootDirectory = DirectoryPointer(
        name="__root__", parent=None, children=[], files=[]
    )

    # Iterate through the lines of puzzle input and assemble the directory structure
    currentDirectory: DirectoryPointer = rootDirectory
    readingLsResponse: bool = False
    for lineNo, line in enumerate(instructions):
        # If line starts with "$", it's a command
        if line.startswith("$"):
            readingLsResponse = False
            command, name = (line + " _").split()[1:3]

            # If cd command, try to chagne the current directory
            if command == "cd":
                if name == "/":
                    currentDirectory = rootDirectory
                elif name == "..":
                    if not currentDirectory.parent:
                        utils.printError(
                            f"#{lineNo + 1}: Current directory '{currentDirectory.name}' has no parent directory."
                        )
                        exit(1)
                    currentDirectory = currentDirectory.parent
                else:
                    for child in currentDirectory.children:
                        if child.name == name:
                            currentDirectory = child
                            break
                    else:
                        utils.printError(
                            f"#{lineNo + 1}: Encountered situation where child directory '{name}' of current directory '{currentDirectory.name}' could not be found"
                        )
                        exit(1)

            # If command is ls, we will start reading contents of the current directory
            elif command == "ls":
                readingLsResponse = True

            else:
                utils.printError(
                    f"#{lineNo + 1}: Unrecognized command '{command}'"
                )

        # If we're reading back contents of a directory
        elif readingLsResponse:
            half1, half2 = line.split()

            # If the line starts with "dir" then we add in a new directory
            if half1 == "dir":
                currentDirectory.children.append(
                    DirectoryPointer(
                        name=half2,
                        parent=currentDirectory,
                        children=[],
                        files=[],
                    )
                )

            # Else, we're creating a new file in the current directory
            else:
                currentDirectory.files.append(
                    FilePointer(name=half2, size=int(half1))
                )

        # Else, we're in an undefined state
        else:
            utils.printError(
                f"#{lineNo + 1}: Directory traversal has encountered an undefined state."
            )

    # Return the root
    return rootDirectory


@utils.part1
def part1(puzzleInput: str):
    # Split the input into lines of commands/output
    instructions = puzzleInput.strip().split("\n")

    # Use the instructions to build out a directory structure
    rootDirectory = createDirectoryStructure(instructions)

    # Find all directories with a total size less than or equal to 100000
    selectedDirectories = [
        d
        for d in rootDirectory.getAllDirectories()
        if d.getTotalSize() <= 100000
    ]

    # The answer is the sum of their sizes
    utils.printAnswer(sum([d.getTotalSize() for d in selectedDirectories]))

    # Pass the directory structure on to part 2
    return rootDirectory


@utils.part2
def part2(_, rootDirectory: DirectoryPointer):
    # Derive the amount of space that needs to be free up from the disk
    totalDiskSize = 70000000
    totalUsedSize = rootDirectory.getTotalSize()
    totalUnusedSize = totalDiskSize - totalUsedSize
    minimumUnusedSize = 30000000
    totalSizeNeeded = minimumUnusedSize - totalUnusedSize

    # Sort all directories by total size
    directoriesBySize = sorted(
        rootDirectory.getAllDirectories(), key=lambda d: d.getTotalSize()
    )

    # Find the first directory that would free up just enough space to meet the minimum
    for directory in directoriesBySize:
        totalSize = directory.getTotalSize()
        if totalSize >= totalSizeNeeded:
            utils.printAnswer(totalSize)
            break


if __name__ == "__main__":
    utils.start()
