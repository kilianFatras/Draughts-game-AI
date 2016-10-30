class Move():
    ''' A move is simply a list of cells which a piece passes by. 
    
    It can be either a CaptureMove or a SimpleMove. 
    These classes do not check whether the list of cells define a valid move'''
    
    def __init__(self, l):
        self.cells = l
            
    def __eq__(self,other):
        return self.cells == other.cells
        
    def __len__(self):
        return len(self.cells)       

       
    def isCapture(self):
        return isinstance(self,CaptureMove)

        
    def toPDN(self):
        s = str(self.cells[0])
        for k in range(1,len(self)):
            s += self.separator+str(self.cells[k])
        return s 
        
    def fromPDN(s):
        moveClass = SimpleMove if s.rfind('-')>-1 else CaptureMove
        cells = [int(i) for i in s.split(moveClass.separator)]
        assert(moveClass == CaptureMove and len(cells)>=2 or len(cells)==2)
        return moveClass(cells)


class CaptureMove(Move):
    separator = "x"
        
    def concat(self, move):
        self.cells += move.cells     
        return self 
          
   
class SimpleMove(Move):
    separator = "-"
        
