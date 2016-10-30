import sys
import time
from IN104_simulateur.gameState import *
from IN104_simulateur.move import *
from random import randint
from IN104_simulateur.cell import Cell

INFINI = 10000000
MAX_STATE = 0
MIN_STATE = 1

class AlphaBetaBrain:
    def __init__(self):
        self.name = "AlphaBetaBrain"
        self.computingTimes = []
        self.maxDeep = 8
        self.verbose = 0

    def play(self, gameState, timeLimit):
        possibleMoves = gameState.getStateMoveDict()
        if self.verbose:
            print("Authorized moves : ")
            for m in possibleMoves.values(): print(m.toPDN())
        try:
            weight, move = self.alphaBeta(gameState, 1, MAX_STATE, -INFINI, INFINI)
            if self.verbose:
                print(self.name + " plays move : " + move.toPDN())

            choice = gameState.doMove(move, inplace = False)
            if str(choice) not in possibleMoves.keys(): raise Exception
        except Exception:
            print(string+' is an invalid move !')
            raise
        return choice

    def alphaBeta(self, gameState, deep, state, alpha, beta):
        """ alpha : best maximum on the path
            beta : best minimum on the path """

        moveDict = gameState.getStateMoveDict()
        if (deep > self.maxDeep or not moveDict):
            return self.eval(gameState),None
        possibleMoves = list(moveDict.values())

        maxWeight = -INFINI
        minWeight = INFINI
        for move in possibleMoves:
            if state == MAX_STATE:
                if alpha < beta:
                    newGameState = gameState.doMove(move)
                    curWeight, curMove = self.alphaBeta(newGameState, deep+1, not state, alpha, beta)
                    if curWeight > maxWeight:
                        maxWeight = curWeight
                        bestMove = move
                        alpha = max(alpha, maxWeight)
            elif state == MIN_STATE:
                if beta > alpha:
                    newGameState = gameState.doMove(move)
                    curWeight,curMove = self.alphaBeta(newGameState, deep+1, not state, alpha, beta)
                    if curWeight < minWeight:
                        minWeight = curWeight
                        bestMove = move
                        beta = min(beta, minWeight)

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
                if Cell.isBlack(cell):
                     nbrBlacks += 1
                elif Cell.isWhite(cell):
                     nbrWhites += 1
            return nbrWhites - nbrBlacks



    def __str__(self):
        return self.name
