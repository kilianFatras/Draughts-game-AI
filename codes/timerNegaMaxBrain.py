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

class TimerAlphaBetaNegaMaxBrain:
    def __init__(self):
        self.name = "timeAlphaBetaBrain"
        self.computingTimes = []
        self.maxTime = 5
        config = {  'nRows': 8, # size of the board
                    'nPieces': 12, # number of pieces at the beginning of the game (should be a multiple of nRows < nRows**2/2)
                    'whiteStarts': True,
                 }
        game = Game(self, 10000, self, 10000, {'nRows':8, 'nPieces': 12}, 1000)

        self.timeMovement =  self.timer(game.gameState)[0]
        self.timeEval = self.timer(game.gameState)[1]


    def timer(self,gameState):
        T=0
        for i in range(15):
            start = time.time()
            stateDict = gameState.findNextStates()
            end = time.time()
            T = T + end-start
            gameState = list(stateDict.values())[0]
        T=T/15
        start1 = time.time()
        self.eval(gameState,MAX_STATE)
        end1 = time.time()
        T1 =  end1 - start1
        return T,T1

    def play(self, gameState, timeLimit):
        START = time.time()
        possibleMoves = gameState.getStateMoveDict()
        print("Authorized moves : ")
        for m in possibleMoves.values(): print(m.toPDN())
        string = ""
        try:
            weight, move = self.alphaBetaNegaMax(gameState, self.maxTime, MAX_STATE, -INFINI, INFINI, 0)
            print(self.name + " plays move : " + move.toPDN())

            choice = gameState.doMove(move, inplace = False)
            if str(choice) not in possibleMoves.keys(): raise Exception
        except Exception:
            print(string+' is an invalid move !')
            raise
        END = time.time()
        print("temps restant : ", self.maxTime - END + START)
        return choice

    def alphaBetaNegaMax(self, gameState, timeLeft, state, alpha, beta, depth):
        """ alpha : best maximum on the path
            beta : best minimum on the path """

        moveDict = gameState.getStateMoveDict()

        possibleMoves = list(moveDict.values())
        nbrMoves = len(possibleMoves)

        if (timeLeft < self.timeEval + nbrMoves * self.timeMovement or not moveDict):
            return self.eval(gameState,state),None

        bestValue = -INFINI
        iMove = 0
        timeLeft = timeLeft-self.timeMovement
        for move in possibleMoves:
            newTime = (timeLeft)/(nbrMoves-iMove) #on réatribue le temps aux autres fils
            start = time.time()
            newGameState = gameState.doMove(move)
            curWeight,curMove = self.alphaBetaNegaMax(newGameState, newTime, not state, -beta, -alpha, depth+1)
            curWeight *= -1
            if bestValue < curWeight:
                bestValue = curWeight
                bestMove = move
            if alpha >= beta:
                return beta, move
            alpha = max(alpha, curWeight)


            end = time.time()
            timeLeft = timeLeft - end + start

            iMove += 1
        return bestValue,bestMove

    def eval(self, gameState, state):
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
            for cell in gameState.boardState.cells:
                if Cell.isBlack(cell):
                     nbrBlacks += 1
                     if Cell.isKing(cell): #une dame vaut 3 pions
                         nbrBlacks += 2
                elif Cell.isWhite(cell):
                     nbrWhites += 1
                     if Cell.isKing(cell): #une dame vaut 3 pions
                         nbrWhites += 2
            if state == MAX_STATE :
                return nbrWhites - nbrBlacks
            else : return -(nbrWhites - nbrBlacks)


    def __str__(self):
        return self.name
