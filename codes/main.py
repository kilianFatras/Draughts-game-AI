import sys
import random

from IN104_simulateur.game import Game
from timerNegaMaxBrain import *
from timerAlphaBetaBrain import *
from alphaBetaBrain import *
from manualBrain import *


def test():
    config = {  'nRows': 8, # size of the board
                'nPieces': 12, # number of pieces at the beginning of the game (should be a multiple of nRows < nRowsÂ²/2)
                'whiteStarts' : True
             }

    manual1 = TimerAlphaBetaBrain()
    manual2 = ManualBrain()

    game = Game(manual1, 1, manual2, 1.5, config, 150) # syntax : Game(ia1, ia2, config [, Nlimit = 150])
    #game.player1.showTime = True # show the time spent by an IA
    #game.player1.timeLimit = 1 # you can change timeLimit per player (unfair game)

    # displayLevel of the game :
    # 0/ does not display anything
    # 1/ displays the board state evolution plus error messages
    # 2/ also displays the list of possible moves
    # 3/ displays everything that is put into the logs
    game.displayLevel = 1
    game.pause = 0
    game.gameState.boardState.debug = False

    pdn = game.runGame()

    return
    # Save logs and pdn in text files
    import datetime as dt
    s = str(dt.datetime.today())
    fileName = str(ia1)+"_vs_"+str(ia2)+"_"+s[s.find(' ')+1:s.find('.')]
    logFile = 'logs/'+fileName+'.log'
    pdnFile = 'pdns/'+fileName+'.pdn'
    with open(logFile, "w") as f:
        f.write(game.log)
    if pdn:
        with open(pdnFile, "w") as f:
            f.write(pdn)
    #'''

    return
    # plot the computation times
    import matplotlib.pylab as plt
    plt.plot(game.player1.computingTimes,'blue')
    plt.plot(game.player2.computingTimes,'red')
    plt.show()


if __name__ == '__main__':
    test()
