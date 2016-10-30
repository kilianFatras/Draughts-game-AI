import sys
import time
from IN104_simulateur.gameState import *
from IN104_simulateur.move import *
from random import randint
from IN104_simulateur.cell import Cell

INFINI = 10000000
MAX_STATE = 0
MIN_STATE = 1

class MinMaxBrain:
    def __init__(self):
        self.name = "minMaxBrain"
        self.computingTimes = []
        self.maxDeep = 4

    def play(self, gameState, timeLimit):
        possibleMoves = gameState.getStateMoveDict()
        print("Authorized moves : ")
        for m in possibleMoves.values(): print(m.toPDN())
        string = ""
        while True:
            try:
                weight, move = self.minMax(gameState, 1, MAX_STATE)
                print(self.name + " plays move : " + string)

                choice = gameState.doMove(move, inplace = False)
                if str(choice) not in possibleMoves.keys(): raise Exception
                break
            except Exception:
                print(string+' is an invalid move !')
                raise

        return choice

    def minMax(self, gameState, deep, state):
        """ Input : state : MAX_STATE or MIN_STATE """
        moveDict = gameState.getStateMoveDict()
        if (deep > self.maxDeep or not moveDict):
            return self.eval(gameState),None
        possibleMoves = list(moveDict.values())

        maxWeight = -INFINI
        minWeight = INFINI
        for move in possibleMoves:
            if state == MAX_STATE:
                newGameState = gameState.doMove(move)
                curWeight, curMove = self.minMax(newGameState, deep+1, not state)
                if curWeight > maxWeight:
                    maxWeight = curWeight
                    bestMove = move
            elif state == MIN_STATE:
                newGameState = gameState.doMove(move)
                curWeight,curMove = self.minMax(newGameState, deep+1, not state)
                if curWeight < minWeight:
                    minWeight = curWeight
                    bestMove = move

        if state == MAX_STATE:
            return maxWeight, bestMove
        elif state == MIN_STATE:
            return minWeight, bestMove

    def eval(self, gameState):
        bigWeight = 1000
        if not gameState.getStateMoveDict():
            hasWon = not gameState.isWhiteTurn
            if hasWon:
                return bigWeight
            else:
                return -bigWeight
        else:
            nbrWhites = 0
            nbrBlacks = 0
            for cell in gameState.boardState.cells:
                if cell.isBlack():
                     nbrBlacks += 1
                elif cell.isWhite():
                     nbrWhites += 1
            return nbrWhites - nbrBlacks



    def __str__(self):
        return self.name
