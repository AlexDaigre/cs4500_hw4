# Alex Daigre
# Aug 27th, 2018
# cs4500
# Version: Python 3.7
# Description:
#   This program simulates a game where the player randomly moves around 
#   a triangular game board. The player can move in four directions: up left,
#   up right, down right, down left. Whenever the player moves to a new position
#   on the board the player markes that positon with a dot. The game ends when
#   all positions have been marked. As the program runs, the game prints the 
#   current position. When the game completes, the program prints some stats
#   about the game that just concluded. When all games have completed, the program 
#   prints some stats about all the games.
# External Files:
#   Standard Library Inputs:
#       Random: Used to generate the random numbers for movements
#       Enum: used to generate the enum for representing movement
#   Output Files:
#       HW3daigreOutfile.txt: This file contains the same output that is printed to 
#       the screen. Detailed above.
# Sources:
#   https://www.w3schools.com/python/python_classes.asp
#   https://stackoverflow.com/questions/11264684/flatten-list-of-lists/11264799
#   https://docs.python.org/3/library/enum.html
#   https://stackoverflow.com/questions/25902690/typeerror-init-takes-0-positional-arguments-but-1-was-given
#   https://docs.python.org/3/tutorial/classes.html
#   https://medium.com/programminginpython-com/python-program-to-find-the-largest-and-smallest-number-in-a-list-fd8fac8aba08
#   https://www.programiz.com/python-programming/methods/built-in/sum
#   https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string

import random
from enum import Enum

# The loop that is executed durring each turn of the game
def gameLoop(gameBoard):
    while gameBoard.isComplete() != True:
        newDirection =  rollDie()
        gameBoard.moveDirection(newDirection)
    return gameBoard

# Rolls a die and returns UL, ER, DL, or DR
def rollDie():
    return Direction(random.randint(1,4))

# Gets a number from the user withion a particular range. 
# prints a particualr message initialy, specified by caller.
def getIntFromUserInRange(message, minValue, maxValue):
    try:
        userInput = int(input(message))
    except:
        pass
    while not (isinstance(userInput, int) and (userInput <= maxValue) and (userInput >= minValue)):
        userInput = input(f"Please enter a number between {minValue} and {maxValue} inclusive:")
        try:
            userInput = int(userInput)
        except:
            pass
    return userInput

# Gets the users choice if they want to run in verbose mode (printing moves as they are made) 
# returns true or false based on users choice
def getVerboseModeFromUser():
    userInput = input("Print moves to the screen as they are made? (y/n):")
    while not ((userInput == "y") or (userInput == "n")):
        userInput = input("Please enter 'y' or 'n':")
    if (userInput == "y"):
        return True
    else:
        return False

#Create a sting with the final game stats
def generateFinalStats(movesOverall, dotsOverall):
    overallMinDots, overallMaxDots, overallAverageDots = getMinMaxAndAverageFromListOfInts(dotsOverall)
    overallMinMoves, overallMaxMoves, overallAverageMoves = getMinMaxAndAverageFromListOfInts(movesOverall)
    return f"""Stats based on all games played: 
        Fewest moves in a single game:{overallMinMoves} 
        Most moves in a single game:{overallMaxMoves} 
        Average moves across all games:{overallAverageMoves} 
        Fewest maximum dots in a single game:{overallMinDots} 
        Most maximum dots in a single game:{overallMaxDots} 
        Average maximum dots across all games:{overallAverageDots}"""


# Generate the minimum, maximum, and average values from a list of ints
def getMinMaxAndAverageFromListOfInts(arrayOfInts):
    average = sum(arrayOfInts, 0) / len(arrayOfInts)
    maximum = max(arrayOfInts)
    minimum = min(arrayOfInts)
    return minimum, maximum, average

# Opens the output file and writes the passed string to it.
def openOutputFileAndWriteContents(outputData):
    fileName = "HW3daigreOutfile.txt"
    with open(fileName, 'w') as outputFile:
            outputFile.write(outputData)

#Enum to represent the direction of movement on our board
class Direction(Enum):
    UL = 1
    UR = 2
    DL = 3
    DR = 4

# The class that determines how the game's board operatates
#  Stores the data on all nodes
class GameBoard:
    # 2D array representing the board. 0,0 starts at one as 
    # this is where the player begins.
    boardSpaces = []
    currentRow = 0
    currentCollumn = 0
    runInVerboseMode = True

    movesLog = ""

    #when class is created log the players starting position
    def __init__(self, numberOfRows, runInVerboseMode):
        self.runInVerboseMode = runInVerboseMode
        self.boardSpaces = []
        for row in range(numberOfRows):
            newList = [0] * (row + 1)
            self.boardSpaces.append(newList)
        self.boardSpaces[0][0] = 1
        startPosition = self.getCurrentPositionAsNumber() 
        self.logMoveData(f"{startPosition}, ")

    # Itterate through all values in boardSpaces and check if they
    #  Have been reached at least once
    def isComplete(self):
        allSpacesVisited = True
        for subList in self.boardSpaces:
            for space in subList:
                if space <= 0:
                    allSpacesVisited = False
                    break
        if allSpacesVisited == True:
            lastposition = self.getCurrentPositionAsNumber()
            self.logMoveData(f"{lastposition}.\n\n")
        return allSpacesVisited

    # Gets the average number of dots on the nodes.
    def getAverageDots(self):
        totalDots = 0
        totalSpaces = 0
        for subList in self.boardSpaces:
            for space in subList:
                totalSpaces += 1
                totalDots += space
        return totalDots/totalSpaces

    # Gets the maximum number of dots on any one node.
    def getMaxDots(self):
        maxDots = 0
        for subList in self.boardSpaces:
            for space in subList:
                if space > maxDots:
                    maxDots = space
        return maxDots

    # Gets the total number of moves performed on the board.
    # This is equal to dots -1 as the board starts with 1 dot.
    def getTotalMoves(self):
        totalMoves = -1
        for subList in self.boardSpaces:
            for space in subList:
                    totalMoves += space
        return totalMoves
    
    # Gets the current position as a sigle number instead of a tuple
    def getCurrentPositionAsNumber(self):
        sumOfPreviousRows = (self.currentRow * (self.currentRow +1)) /2
        currentPosition = sumOfPreviousRows + (self.currentCollumn + 1)
        return currentPosition

    #combines the actions of printing and recording log data, for convience.
    def logMoveData(self, dataToLog):
        if (self.runInVerboseMode == True):
            print(dataToLog, end = "")
            self.movesLog += dataToLog

    # Get the value of the next position requested.
    # Check if that value is valid.
    # If not add one to current position and exit.
    # If change current position and add one to new position.
    def moveDirection(self, direction):
        newRow = self.currentRow
        newCollumn = self.currentCollumn

        # Find new row
        if direction == Direction.UL or direction == Direction.UR:
            newRow -= 1
        elif direction == Direction.DL or direction == Direction.DR:
            newRow += 1

        # Find new collumn. No change in collumn number on DL or UR.
        if direction == Direction.UL:
            newCollumn -= 1
        elif direction == Direction.DR:
            newCollumn += 1
        
        # Check if our location is out of bounds, if so add 1 to 
        #  current space and return.
        if newRow < 0 or newRow > (len(self.boardSpaces) - 1):
            self.boardSpaces[self.currentRow][self.currentCollumn] += 1
            currentPosition = self.getCurrentPositionAsNumber()
            self.logMoveData(f"{currentPosition}, ")
            return
        elif newCollumn < 0 or newCollumn > newRow:
            self.boardSpaces[self.currentRow][self.currentCollumn] += 1
            currentPosition = self.getCurrentPositionAsNumber()
            self.logMoveData(f"{currentPosition}, ")
            return

        # Set new row and collumn and add to the new position
        self.currentRow = newRow
        self.currentCollumn = newCollumn
        self.boardSpaces[self.currentRow][self.currentCollumn] += 1
        currentPosition = self.getCurrentPositionAsNumber()
        self.logMoveData(f"{currentPosition}, ")
        return


# Main code
# Log and print intro info
logToFile = ""
programIntro = "This program simulates a game where the player randomly moves around a triangular game board. The player can move in four directions: up left, up right, down right, down left. Whenever the player moves to a new position on the board the player markes that positon with a dot. The game ends when all positions have been marked. As the program runs, the game prints the current position. When the game completes, the program prints some stats about the game that just concluded.\n"
movesOverall = []
dotsOverall = []
logToFile += programIntro + "\n"
print(programIntro)
# Initialise the gameboard
boardSize = getIntFromUserInRange("Specify a size for the board:", 2, 25)
numberOfRuns = getIntFromUserInRange("Specify a number of runs:", 10, 50)
verboseChoise = getVerboseModeFromUser()
for n in range(numberOfRuns):  
    gameBoard = GameBoard(boardSize, verboseChoise)
    # Initialise game loop
    gameBoard = gameLoop(gameBoard)
    # log and print end info
    logToFile += gameBoard.movesLog
    gameStats = f"Total moves: {gameBoard.getTotalMoves()}\nAverage number of dots: {gameBoard.getAverageDots()}\nMaximum number of dots: {gameBoard.getMaxDots()}"
    movesOverall.append(gameBoard.getTotalMoves())
    dotsOverall.append(gameBoard.getMaxDots())
    logToFile += gameStats
    print(gameStats)
finalStats = generateFinalStats(movesOverall, dotsOverall)
logToFile += finalStats
print(finalStats)
#print loged data to file
openOutputFileAndWriteContents(logToFile)