import sys
import time
from IN104_simulateur.gameState import *
from IN104_simulateur.move import *
from random import randint
from IN104_simulateur.cell import Cell
from IN104_simulateur.game import *

INFINI = 10000000
MAX_STATE = 0
MIN_STATE = 1

class TimerAlphaBetaBrain:
    def __init__(self, name = "DaTApage", config="jaiperdu"):
        self.name = name
        self.computingTimes = []
        config = {  'nRows': 8, # size of the board
                    'nPieces': 12, # number of pieces at the beginning of the game (should be a multiple of nRows < nRows**2/2)
                    'whiteStarts': True,
                 }
        game = Game(self, 1.5, self, 1.5, {'nRows':8, 'nPieces': 12}, 1000)
        self.timeMovement =  self.timer(game.gameState)[0]
        self.timeEval = self.timer(game.gameState)[1]


    def timer(self,gameState):
        """ Compute the time of one movement (the time to get the next states)
        and the time of the eval function
        Output : (timeMovement, timeEval)"""
        T=0
        for i in range(15):
            # Compute timeMovement
            start = time.time()
            stateDict = gameState.findNextStates()
            end = time.time()
            timeMovement = timeMovement + end-start
            gameState = list(stateDict.values())[0]

            # Compute timeEval
            start1 = time.time()
            self.eval(gameState)
            end1 = time.time()
            timeEval =  end1 - start1
        timeMovement /= 15
        timeEval /= 15
        return timeMovement,timeEval

    def play(self, gameState, deadline):
        possibleMoves = gameState.getStateMoveDict()

        try:
            weight, move = self.alphaBeta(gameState, -deadline.until(), MAX_STATE, -INFINI, INFINI, 0)

            choice = gameState.doMove(move, inplace = False)
            if str(choice) not in possibleMoves.keys(): raise Exception
        except Exception:
            raise

        return choice

    def alphaBeta(self, gameState, timeLeft, state, alpha, beta, depth):
        """ alpha : best maximum on the path
            beta : best minimum on the path """
        #tempsIni = timeLeft
        moveDict = gameState.getStateMoveDict()

        possibleMoves = list(moveDict.values())
        nbrMoves = len(possibleMoves)
        iMove = 0

        if (timeLeft < self.timeEval + nbrMoves * self.timeMovement or nbrMoves == 0):
            return self.eval(gameState),None

        maxWeight = -INFINI
        minWeight = INFINI
        for move in possibleMoves:
            if iMove == 0 and nbrMoves > 3:
                newTime = timeLeft/5
#on réaloue plus de temps à la première branche car sinon ce n'est pas équitable par rapport aux autres et on ne l'explore pas assez, pour cela, si il y a plus de 3 fils,
#on divise arbitrairement par 4
            else:
                newTime = timeLeft/(nbrMoves-iMove)

            begin = time.time()
            if state == MAX_STATE:
                if alpha < beta:
                    newGameState = gameState.doMove(move)
                    curWeight, curMove = self.alphaBeta(newGameState, newTime, not state, alpha, beta, depth+1)
                    if curWeight > maxWeight:
                        maxWeight = curWeight
                        bestMove = move
                        alpha = max(alpha, maxWeight)

            elif state == MIN_STATE:
                if beta > alpha:
                    newGameState = gameState.doMove(move)
                    curWeight,curMove = self.alphaBeta(newGameState, newTime, not state, alpha, beta, depth+1)
                    if curWeight < minWeight:
                        minWeight = curWeight
                        bestMove = move
                        beta = min(beta, minWeight)
            stop = time.time()
            timeLeft = timeLeft - stop + begin
            iMove += 1
        if state == MAX_STATE:
            return maxWeight, bestMove
        elif state == MIN_STATE:
            return minWeight, bestMove

    def eval(self, gameState):
        """ Evaluation function
        Consider the difference between #whites and #blacks. Each king is considered
        as 3.5 checkers. A non-king checker on the border is considered as 1.75 checkers
        (because it's more protected on a border)"""
        
        if not gameState.getStateMoveDict():
            bigWeight = 1000
            hasWon = not gameState.isWhiteTurn
            if hasWon:
                return bigWeight
            else:
                return -bigWeight
        else:
            nbrWhites = 0
            nbrBlacks = 0
            index=gameState.boardState.indexToRC
            row = 0
            column = 0
            for cell in gameState.boardState.cells:
                row = row%gameState.boardState.nRows + 1
                column = column%gameState.boardState.nRows + 1
                if Cell.isBlack(cell):
                     nbrBlacks += 1
                     if Cell.isKing(cell): #une dame vaut 3.5 pions
                         nbrBlacks += 2.5
                     elif column == 0 or column == gameState.boardState.nRows - 1 or row == gameState.boardState.nRows - 1 or row == 0:
                         nbrBlacks += 0.75 #se trouver sur les bords vaut 0.75 pts sauf si c'est une dame
                elif Cell.isWhite(cell):
                     nbrWhites += 1
                     if Cell.isKing(cell): #une dame vaut 3.5 pions
                         nbrWhites += 2.5
                     elif column == 0 or column == gameState.boardState.nRows - 1 or row == gameState.boardState.nRows - 1 or row == 0:
                         nbrWhites += 0.75 #se trouver sur les bords vaut 0.75 pts sauf si c'est une dame

            return nbrWhites - nbrBlacks



    def __str__(self):
        return self.name
