from .boardState import *
from .move import *

class GameState:
    ''' The GameState gathers the state of the board plus some auxilliary info like whose turn to play and info to know if it is a draw '''

    def __init__(self, config = None):
        if config:
            self.boardState = BoardState(config['nRows'], config['nPieces'])
            self.isWhiteTurn = config['whiteStarts']
            self.noCaptureCounter = 0
   
    def copy(self):
        copy = GameState()
        copy.boardState = self.boardState.copy()
        copy.isWhiteTurn = self.isWhiteTurn
        copy.noCaptureCounter = self.noCaptureCounter
        return copy
   
                
    def findPossibleMoves(self):
        return self.boardState.findPossibleMoves(self.isWhiteTurn) 
           
    def doMove(self, move, inplace = False):
        if inplace:
            gs = self
        else:
            gs = GameState()
            gs.boardState = self.boardState.copy() 
        gs.boardState.doMove(move) # boardState's doMove is always in-place
        gs.noCaptureCounter = 0 if move.isCapture() else self.noCaptureCounter+1
        gs.isWhiteTurn = not self.isWhiteTurn
        return gs
      
    def findNextStates(self):
        moves =  self.findPossibleMoves()
        nextStates = {}
        for move in moves:
            state = self.doMove(move)
            nextStates[ str(state) ] = state
        return nextStates     

    def getStateMoveDict(self):
        moves =  self.findPossibleMoves()
        nextStates = {}
        for move in moves:
            nextStates[ str(self.doMove(move)) ] = move
        return nextStates 

                  
    def reverse(self):
        self.boardState.reverse()
        self.isWhiteTurn = not self.isWhiteTurn
      
    def __str__(self):
        s = 'W' if self.isWhiteTurn else 'B'
        s+= str(self.boardState)
        s+= str(self.noCaptureCounter)
        return s

    def toDisplay(self, showBoard = False):
        s = self.boardState.toDisplay(showBoard)+'\n'
        s += 'White' if self.isWhiteTurn else 'Black'
        s += "'s turn to play."
        return s
        
    def display(self, showBoard = False):
        print(self.toDisplay(showBoard))

