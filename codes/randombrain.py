import sys
import time
from random import randint
import math
from IN104_simulateur.game import *
from IN104_simulateur.move import *


class RandomBrain :
    def __init__(self,name):
        self.name = name
        self.computingTimes = []

    def play(self, gameState,timeLimit) :
        possibleMoves = gameState.getStateMoveDict()
        print("Authorized moves : ")
        for m in possibleMoves.values(): print(m.toPDN())
        string = ""
        while True:
            try:
                print(self.name + "plays move " ,end ="")
                #time.sleep(1)

                string = self.randomString(list(possibleMoves.values()))
                print(string)
                move = Move.fromPDN(string)
                choice = gameState.doMove(move, inplace = False)
                if str(choice) not in possibleMoves.keys(): raise Exception
                break
            except TimeOutException as e:
                print('Sorry, you took to much time to think !')
                raise e
            except Exception as e:
                print(string+' is an invalid move !')
                print(e)

        return choice

    def randomString (self, possibleMovesList) :
        coup = randint(0,len(possibleMovesList)-1)
        return possibleMovesList[coup].toPDN()
