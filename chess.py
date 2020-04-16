class Chessboard:
    def __init__(self):
        self.chessboard=[["r","n","b","q","k","b","n","r"],
                         ["p","p","p","p","p","p","p","p"],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".","P",".",".","."],
                         ["P","P","P","P","P","P","P","P"],
                         ["R","N","B","Q","K","B","N","R"]]
        self.turn="white"
        self.end=False
        self.possibleMoves={"k":[["noCheck",x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]], # castling to implement
                             "q":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==y or x==0 or y==0) and [x,y]!=[0,0]],
                             "r":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==0 or y==0) and [x,y]!=[0,0]], # castling to implement
                             "b":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if x==y!=0],
                             "k":[["notTeammate",x,y] for [x,y] in [[-2,-1],[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2]]],
                             "p":[["notTeammate",-1,0],["noPieceBetween+onRow/2",-2,0],["enemyOnly",-1,-1],["enemyOnly",-1,1]]} # add support for black pawns
    
    
    def chessToList(self,coord):
        self.x=8-int(coord[1])
        self.y=ord(coord[0])-97
        return self.x,self.y
    
    
    def noCheck(self,xStart,yStart,_,__):
        check=False
        for x in range(8):
            for y in range(8):
                square=self.chessboard[x][y]
                if square!=".":
                    for move in self.possibleMoves[square.lower()]:
                        if self.moveAllowed(move) and x+move[1]==xStart and y+move[2]==yStart:
                            return False
        return True
    
    def notTeammate(self,_,__,xFinish,yFinish):
        square=self.chessboard[xFinish][yFinish]
        if (square.isupper() and self.turn=="white") or (square.islower() and self.turn=="black"):
            return False
        return True
    
    def noPieceBetween(self,xStart,yStart,xFinish,yFinish):
        if xStart==xFinish: # horizontal
            if yStart<yFinish and self.chessboard[xStart][yStart+1:yFinish]==["."]*(yFinish-yStart+1):
                return True
            elif yFinish<yStart and self.chessboard[xStart][yFinish+1:yStart]==["."]*(yStart-yFinish+1):
                return True
            return False
        elif yStart==yFinish: # vertical
            if xStart<xFinish:
                squareStripe=range(xStart+1,xFinish)
            else:
                squareStripe=range(xFinish+1,xStart)
            for x in squareStripe:
                if self.chessboard[x][yStart]!=".":
                    return False
            return True
        else: # diagonal
            if xStart>xFinish:
                for diff in range(xStart-xFinish+1):
                    if self.chessboard[xFinish+diff][yFinish+diff]!=".":
                        return False
            else:
                for diff in range(xFinish-xStart+1):
                    if self.chessboard[xStart+diff][yStart+diff]!=".":
                        return False
            return True
    
    def enemyOnly(self,_,__,xFinish,yFinish):
        square=self.chessboard[xFinish][yFinish]
        if (square.isupper() and self.turn=="black") or (square.islower() and self.turn=="white"):
            return True
        return False
    
    def onRow(self,xStart,yStart,_,__,nRow):
        if 8-xStart==nRow:
            return True
        return False
    
    
    def moveAllowed(self,xStart,yStart,xFinish,yFinish,piece):
        for square in [xStart,yStart,xFinish,yFinish]:
            if square<0 or square>7:
                return False
        xDiff,yDiff=xFinish-xStart,yFinish-yStart
        
        foundMove=False
        for moveTest in self.possibleMoves[piece.lower()]:
            if [moveTest[1],moveTest[2]]==[xDiff,yDiff]:
                move=moveTest
                foundMove=True
                break
        if not foundMove:
            return False
        
        functionAnswers=[]
        for condition in move[0].split("+"):
            condition=condition.split("/")
            toExec="self."+condition[0]+"(xStart,xFinish,yStart,yFinish"
            try: toExec+=","+condition[1]+")"
            except: toExec+=")"
            functionAnswers.append(eval(toExec))
        if False in functionAnswers:
            return False
        return True
    
    def movePiece(self):
        print()
        for ligne in self.chessboard:
            print("".join(ligne))
        print()
        move=input("Move : ") # To implement in a better way
        start,finish=move[:2],move[2:]
        xStart,yStart=self.chessToList(start)
        xFinish,yFinish=self.chessToList(finish)
        piece=self.chessboard[xStart][yStart]
        if self.moveAllowed(xStart,yStart,xFinish,yFinish,piece):
            self.chessboard[xFinish][yFinish]=piece
            self.chessboard[xStart][yStart]="."

chessboard=Chessboard()
while True:
    chessboard.movePiece()
