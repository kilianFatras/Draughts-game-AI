from enum import Enum

class Cell(Enum):
    ''' This enumeration represents the possible states of a cell on the board '''
    empty = (None,None)
    w = (True,False)
    W = (True,True)
    b = (False,False)
    B = (False,True)

    def isWhite(self):
        return self is Cell.w or self is Cell.W

    def isBlack(self):
        return self is Cell.b or self is Cell.B

    def isMan(self):
        return self is Cell.w or self is Cell.b

    def isKing(self):
        return self.value[1]

    def invertColor(self):
        return Cell.empty if self is Cell.empty else Cell( (not self.value[0], self.isKing() ) )

    def promoted(self):
        return Cell.empty if self is Cell.empty else Cell( (self.value[0], True) )

    def __str__(self):
        if self is Cell.empty:
            return '.'
        else:
            return self.name
