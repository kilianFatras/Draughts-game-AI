import sys
import time
from .gameState import *
from .move import *
from .player import TimeOutException

class ManualBrain:

    def __init__(self):
        print("Please enter your name")
        self.name = sys.stdin.readline()[0:-1] 
        self.computingTimes = []
        self.alwaysWhite = False
    
    def play(self, gameState, timeLimit):
        possibleMoves = gameState.getStateMoveDict()
        print("Authorized moves : ")
        for m in possibleMoves.values(): print(m.toPDN())
        string = ""
        while True: 
            try:   
                print("Please enter a move")
                string = sys.stdin.readline()[0:-1]
                move = Move.fromPDN(string)
                choice = gameState.doMove(move, inplace = False)
                if str(choice) not in possibleMoves.keys(): raise Exception
                break
            except TimeOutException as e:
                print('Sorry, you took to much time to think !')
                raise e
            except Exception:
                print(string+' is an invalid move !')
            
        return choice

          
    def __str__(self):
        return self.name
    

