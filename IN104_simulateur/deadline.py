import time
class Deadline:
    
    def __init__(self, time):
        self.time = time
        
    def until(self):
        return time.time()-self.time
