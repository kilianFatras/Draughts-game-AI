import signal
import time
import math
from .cell import *
from .gameState import *
from .deadline import *

# Register an handler for the timeout
def playTimeOutHandler(signum, frame):
    raise TimeOutException("Player takes too long to make a decision.")
    
signal.signal(signal.SIGALRM, playTimeOutHandler)


class Player:
    ''' Class encapsulating the artificial intelligence, making the interface between the latter and a game
    inputs:
        - brain: the artificial intelligence. It must implement 
                * a method "play" taking a gameState and returning one of the reachable gameState
                * the method __str__ defining the name of the ai
        - isWhite: true if the player is the white one  
    '''

    def __init__(self, isWhite, brain, timeLimit):
        self.isWhite = isWhite
        assert brain, "Player needs a brain !"
        self.brain = brain
        self.timeLimit = timeLimit
        self.computingTimes = [] # store the computing time for each move
        self.showTime = False
        try:
            self.alwaysSeeAsWhite = self.brain.alwaysSeeAsWhite
        except:
            self.alwaysSeeAsWhite = True
        
    
    def play(self, gameState):
        reverse = (not self.isWhite) and self.alwaysSeeAsWhite        
        if reverse: gameState.reverse()
        
        if self.timeLimit and self.timeLimit>0:  
            # signals only take an integer amount of seconds, so I have to ceil the time limit
            signal.alarm(math.ceil(self.timeLimit+0.01))
        
        try:
            t1 = time.time()    
            deadline = Deadline(t1+self.timeLimit) if self.timeLimit else None 
            chosenState = self.brain.play(gameState, deadline)
            length = time.time()-t1
        except Exception as e:
            raise e
        signal.alarm(0) 
               
        if self.timeLimit and length>(self.timeLimit+0.01):
            raise TimeOutException(str(self)+' took too much time to make a decision : '+str(length)+' sec')
        self.computingTimes.append(length)
        if self.showTime:
            print(str(self)+" took "+'{:.3f}'.format(length)+"s to make a decision")
                
        if reverse: chosenState.reverse()
        return str(chosenState)
   
    
    def name(self):
        return str(self.brain)
     
    def __str__(self):
        return ("White" if self.isWhite else "Black")+' ('+self.name()+')'
        
          
# Unhandled exception leading to the game interuption    
class TimeOutException(Exception):
    def __init__(self, message):
        self.message = message
