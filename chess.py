class Chessboard():
    def __init__(self):
        self.chessboard=[["r","n","b","q","k","b","n","r"],
                         ["p","p","p","p","p","p","p","p"],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".","."],
                         ["P","P","P","P","P","P","P","P"],
                         ["R","N","B","Q","K","B","N","R"]]
        self.turn="white"
        self.end=False
        self.possibleMoves={"k":[["noCheck",x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]], # castling to implement
                             "q":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==y or x==0 or y==0) and [x,y]!=[0,0]],
                             "r":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==0 or y==0) and [x,y]!=[0,0]],
                             "b":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if x==y!=0],
                             "k":[["notTeammate",x,y] for [x,y] in [[-2,-1],[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2]]],
                             "p":[["notTeammate",-1,0],["noPieceBetween+onRow/2",-2,0],["enemyOnly",-1,-1],["enemyOnly",-1,1]]}
    
    
    def chessToList(self,coord):
        self.x=8-int(coord[1])
        self.y=ord(coord[0])-97
        return self.x,self.y
    
    
    def noCheck(self,xFinish,yFinish):
        check=False
        for xStart in range(8):
            for yStart in range(8):
                square=self.chessboard[xStart][yStart]
                if square!=".":
                    for move in possibleMoves[square.lower()]:
                        if moveAllowed(move) and xStart+move[1]==xFinish and yStart+move[2]==yFinish:
                            check=True
                            break
                    if check: break
            if check: break
        return not check

    def notTeammate(self,xFinish,yFinish):
        square=self.chessboard[x][y]
        if (square.isupper() and self.turn=="white") or (square.islower() and self.turn=="black"):
            return False
        else:
            return True

    def noPieceBetween(self,xStart,yStart,xFinish,yFinish):
        if xStart==xFinish:
            pass # horizontal
        elif yStart==yFinish:
            pass # vertical
        elif xStart-xFinish==yStart-yFinish:
            pass # diagonal

    def enemyOnly(self,xFinish,yFinish):
        square=self.chessboard[xFinish][yFinish]
        if (square.isupper() and self.turn=="black") or (square.islower() and self.turn=="white"):
            return True
        else:
            return False

    def onRow(self,xStart,yStart,nRow):
        if x==nRow:
            return True
        else:
            return False
    
    
    def moveAllowed(self,move):
        pass
    
    def movePiece(self,move):
        self.start,self.finish=move[:2],move[2:]
        self.xStart,self.yStart=self.chessToList(start)
        self.xFinish,self.yFinish=self.chessToList(finish)
        move=input("Move : ") # To implement in a better way
        if moveAllowed(move):
            self.chessboard[xFinish][yFinish]=self.chessboard[xStart][yStart]
            self.chessboard[xStart][yStart]="."
