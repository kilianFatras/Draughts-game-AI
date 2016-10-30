from .cell import *
from .move import *    
    
class BoardState:
    ''' Represents a board state
     
     * Cells are numbered as follows (example for a 8x8 board with 12 pieces):
     *
     *    col 0  1  2  3  4  5  6  7
     * row  -------------------------  row
     *  0  |     0     1     2     3 |  0
     *  1  |  4     5     6     7    |  1
     *  2  |     8     9    10    11 |  2
     *  3  | 12    13    14    15    |  3
     *  4  |    16    17    18    19 |  4
     *  5  | 20    21    22    23    |  5
     *  6  |    24    25    26    27 |  6
     *  7  | 28    29    30    31    |  7
     *      -------------------------
     *    col 0  1  2  3  4  5  6  7
     *
     * The starting board looks like this:
     *
     *    col 0  1  2  3  4  5  6  7
     * row  -------------------------
     *  0  |    bb    bb    bb    bb |  
     *  1  | bb    bb    bb    bb    |  
     *  2  |    bb    bb    bb    bb |  
     *  3  | ..    ..    ..    ..    |  
     *  4  |    ..    ..    ..    .. |  
     *  5  | ww    ww    ww    ww    |  
     *  6  |    ww    ww    ww    ww |  
     *  7  | ww    ww    ww    ww    |  
     *      -------------------------
     *        0  1  2  3  4  5  6  7
     *
     * The black player starts from the top of the board (row 0,1,2)
     * The white player starts from the bottom of the board (row 5,6,7)
    '''   
    
    def __init__(self, nRows = None, nPieces = None):
        if nRows and nPieces:
            self.debug = False
            self.nRows = nRows
            self.nPieces = nPieces
            self.nCells = (self.nRows**2)//2
            self.cells = [Cell.b]*self.nPieces + [Cell.empty]*(self.nCells-2*self.nPieces) + [Cell.w]*self.nPieces
        
    def copy(self):
        copy = BoardState()
        copy.debug = self.debug
        copy.nRows = self.nRows
        copy.nPieces = self.nPieces
        copy.nCells = self.nCells
        copy.cells = self.cells.copy()
        return copy
                       
    def __eq__(self,other):
        return (self.cells == other.cells)
              
        
    def reverse(self):
        '''Return the state resulting from rotating the board by 180° and swapping black and white pieces'''
        x = None
        for i in range(self.nCells//2):
            x = self.cells[i]
            self.cells[i] = self.cells[self.nCells-i-1].invertColor() 
            self.cells[self.nCells-i-1] = x.invertColor()                    
        return self

        
    def indexToRC(self,i):
        ''' Convert and index (from 0 to nCells-1) to a couple (row, column), each being beetween 0 and nRows-1.
        
        The origin and axes orientation is given by the figure at the top of this file.'''
        #assert i in range(self.nCells), 'Non valid cell index : '+str(i)
        r = i//(self.nRows//2)
        c = 2*(i%(self.nRows//2)) + (r+1)%2
        return (r,c)
    
    def isValidRC(self,r,c):
        return (r in range(self.nRows) and c in range(self.nRows) and r%2 != c%2)
        
    def RCtoIndex(self,r,c):
        ''' Convert a row,column coordinate into a linear index.'''
        #assert self.isValidRC(r,c), 'Non valid cell coordinates :'+str(r)+","+str(c)
        return r*(self.nRows//2) + c//2
        
        
    def getCell(self,r,c):
        ''' Return the content of a cell located by its coordinates '''
        return self.cells[self.RCtoIndex(r,c)]
        
    def setCell(self,r,c, cell):
        ''' Return the content of a cell located by its coordinates '''
        self.cells[self.RCtoIndex(r,c)] = cell
    
        
    def __str__(self):
        '''Return a string representation of the state suitable for state recording'''
        return ''.join(map(str,self.cells))
    
    
    def display(self, showBoard = False):
        print(self.toDisplay(showBoard))
        
    def toDisplay(self, showBoard = False):
        ''' Return a string suitable for state visualization in text mode (like the one at the top of this file) 
        If showBard is True, then a board with cell indices is shown next to the state'''
        
        formater = '{0:3d}'
        
        s = ","+('---'*self.nRows)+","
        if showBoard:
            s+= "    ,"+('---'*self.nRows)+","
        s +="\n"
        for r in range(self.nRows):
            s+='|'
            for c in range(self.nRows):
                if c%2 != r%2:
                    s+=' '+str(self.getCell(r,c))+' '
                else:
                    s+='   '
            s+='|'
            if showBoard:
                s+='    |'
                for c in range(self.nRows):
                    if c%2 != r%2:
                        s+=formater.format(self.RCtoIndex(r,c))
                    else:
                        s+='   '
                s+='|'
            
            s+='\n'
        s+= "'"+('---'*self.nRows)+"'" 
        if showBoard:
            s+= "    '"+('---'*self.nRows)+"'"
        s+='\n'                
        return s
        
        
    def viewBoard(self):
        formater = '{0:3d}'
        
        s = ","+('---'*self.nRows)+",\n"
        for r in range(self.nRows):
            s+='|'
            for c in range(self.nRows):
                if c%2 != r%2:
                    s+=formater.format(self.RCtoIndex(r,c))
                else:
                    s+='   '
            s+='|\n'            
        s+= "'"+('---'*self.nRows)+"'\n"        
        print(s)
                       
        
    def getPositions(self, white):
        '''Return an iterator over men and kings position of the given color'''
        function = Cell.isWhite if white else Cell.isBlack
        for i in range(self.nCells):
            if function(self.cells[i]): yield i

        
    def tryJumpFrom(self, cellIndex, piece = None, previousCaptures = []):
        ''' Find capturing moves that a iece located at a given position.
        
        Inputs:
            - cellIndex : the starting position on the board.
            - piece: the type of piece being moved
        Output:
            - moves: a list of valid variations. A variation is a list of jumps
         '''
        
        if self.debug:
            tabs = '    '*len(previousCaptures)
            print(tabs,'depth of call ', len(previousCaptures))
            print(tabs,'cellIndex : ', cellIndex)
            print(tabs,'previousCaptures : ', previousCaptures)
            print()
            
        rootCall = piece is None
        if rootCall: 
            # we temporally remove the piece from the board so that it can perform a rafle if possible
            piece = self.cells[cellIndex] 
            self.cells[cellIndex] = Cell.empty
            assert (piece is not Cell.empty), 'Error, the starting position contains no piece'
            
        (r0,c0) = self.indexToRC(cellIndex)             
        possibleVariations = [] # a list of Move objects that the piece can perform starting from this place (these moves do not include the starting point)
        for tr in [-1,1]:
            for tc in [-1,1]:
                r1, c1 = r0+tr, c0+tc
                r2, c2 = r0+2*tr, c0+2*tc
                if not self.isValidRC(r2,c2): continue                
                jumpPos = self.RCtoIndex(r1,c1)
                newPos = self.RCtoIndex(r2,c2)                  
                if jumpPos in previousCaptures: continue
                
                isWhite = piece.isWhite()
                jumpedCell = self.getCell(r1,c1)                   
                if jumpedCell.value[0] == (not isWhite) and (self.cells[newPos] == Cell.empty): 
                    # if this is a valid jump
                    if not piece.isKing() and ((r2==0 and isWhite) or (r2==self.nRows-1 and not isWhite)): 
                        # if a man has reached the last row, it has to stop and be crowned
                        possibleVariations.append( CaptureMove([newPos]) )
                    else:
                        newPreviousCaptures = previousCaptures + [jumpPos]
                        possibleVariations += self.tryJumpFrom(newPos, piece, newPreviousCaptures)
        
        if self.debug:
            print(tabs,'possible variations before taking the max :')
            for move in possibleVariations:print(tabs, move.toPDN())    
            print() 
        
        # Once we've gathered all possible variations from the four adjacent cells, we keep only the longest ones
        currentMax = 0
        longestVariations = []
        for variation in possibleVariations:
            if len(variation)>currentMax:
                currentMax = len(variation)
                longestVariations = [variation]
            elif len(variation)>=currentMax:                            
                longestVariations.append(variation)
        
        # Then we insert the starting point to at the beginning of all variations kept        
        moves = []
        for variation in longestVariations:
            moves.append( CaptureMove([cellIndex]).concat(variation) )
        
        # we reset the cell to its initial piece
        if rootCall:
            self.cells[cellIndex] = piece 
        # if there is no move possible from this cellIndex but that is not the rootCall,
        # then it means cellIndex is the end of a move and we need to put it in the possible moves
        elif not moves:
            moves = [CaptureMove([cellIndex])]
        
        if self.debug:
            print(tabs,'possible ends of the move :')
            for move in moves:print(tabs, move.toPDN())    
            print() 
            
        return moves
    
    
    def tryMoveFrom(self, cellIndex):
        ''' Simply find authorized moves of a given piece at position cllIndex on the board '''
        piece = self.cells[cellIndex]
        assert (piece is not Cell.empty), 'Error, the starting position contains no piece'
        
        (r0,c0) = self.indexToRC(cellIndex)
        # trs store valid row movements (downward for blacks, upward for whites, an both for kings)   
        trs = [-1,1] if piece.isKing() else [-1 if piece.isWhite() else 1] 
             
        possibleMoves = []        
        for tr in trs:
            for tc in [-1,1]:
                r1, c1 = r0+tr, c0+tc
                if not self.isValidRC(r1,c1): continue # if the new position candidate is outside the board
                 
                newPos = self.RCtoIndex(r1,c1)                       
                if self.cells[newPos] is Cell.empty:
                    possibleMoves.append( SimpleMove([cellIndex, newPos]) )
                       
        return possibleMoves
        
    def findPossibleMoves(self, color):
        '''Find valid moves and their corresponding states for a given player.
        
        Input: 
            - color: the color of the player we want to find moves
        Outputs:
            - moves: the list containing very authhorized move.
        
        '''       
        moves = []
        
        # First we look for capturing moves (we are obliged to capture as many pieces as possible)
        maxCaptures = 0
        for position in self.getPositions(color):
            pieceMoves = self.tryJumpFrom(position)
            
            if pieceMoves:
                if len(pieceMoves[0])>maxCaptures:
                    moves = pieceMoves
                    maxCaptures = len(pieceMoves[0])
                elif len(pieceMoves[0])==maxCaptures:
                    moves += pieceMoves
                             
        # If there is no capture move possible, we find simple moves                   
        if not moves:
            for position in self.getPositions(color):
                moves = moves + self.tryMoveFrom(position)    
        
        return moves


    def doMove(self, move):
        ''' Update the state according to the specified move 
        
        Note that this function does not check if the move is valid'''
        
        start, end = move.cells[0], move.cells[len(move)-1]        
        piece = self.cells[start]
                
        if isinstance(move,SimpleMove):
            nextR, nextC = self.indexToRC(end)
            self.cells[start] = Cell.empty
            self.cells[end] = piece
            
        elif isinstance(move,CaptureMove):
            initP = start
            initR, initC = self.indexToRC(initP)
            for k in range(1,len(move)):
                nextP = move.cells[k]
                nextR, nextC = self.indexToRC(nextP)
                jumpedR, jumpedC = (nextR+initR)//2, (nextC+initC)//2 
                self.setCell(jumpedR,jumpedC,Cell.empty)
                initR, initC = nextR, nextC
            self.cells[start] = Cell.empty
            self.cells[end] = piece
        else:
            raise Exception('Invalid argument, CaptureMove or SimpleMove expected')
                
        if (piece.isWhite() and nextR==0) or (piece.isBlack() and nextR==self.nRows-1):
            self.cells[end] = piece.promoted()
    
        return self    
        
