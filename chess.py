class Chessboard:
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
                             "r":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==0 or y==0) and [x,y]!=[0,0]], # castling to implement
                             "b":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if x==y!=0],
                             "k":[["notTeammate",x,y] for [x,y] in [[-2,-1],[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2]]],
                             "p":[["notTeammate",-1,0],["noPieceBetween+onRow/2",-2,0],["enemyOnly",-1,-1],["enemyOnly",-1,1]]}
    
    
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
                    for move in possibleMoves[square.lower()]:
                        if moveAllowed(move) and x+move[1]==xStart and y+move[2]==yStart:
                            check=True
                            break
                    if check: break
            if check: break
        return not check
    
    def notTeammate(self,_,__xFinish,yFinish):
        square=self.chessboard[x][y]
        if (square.isupper() and self.turn=="white") or (square.islower() and self.turn=="black"):
            return False
        else:
            return True
    
    def noPieceBetween(self,xStart,yStart,xFinish,yFinish):
        if xStart==xFinish: # horizontal
            if yStart<yFinish and self.chessboard[xStart][yStart+1:yFinish]==[""]*(yFinish-yStart+1):
                return True
            elif yFinish<yStart and self.chessboard[xStart][yFinish+1:yStart]==[""]*(yStart-yFinish+1):
                return True
            else:
                return False
        elif yStart==yFinish: # vertical
            if xStart>xFinish:
                squareStripe=range(xStart+1,xFinish)
            else:
                squareStripe=range(xFinish+1,xStart)
            for x in squareStripe:
                if self.chessboard[x][yStart]!=".":
                    return False
            return True
        else: # diagonal (not finished)
            if xStart>xFinish:
                for diff in range(xStart-xFinish+1):
                    if self.chessboard[x+diff][y+diff]!=".":
                        return False
            return True
    
    def enemyOnly(self,_,__xFinish,yFinish):
        square=self.chessboard[xFinish][yFinish]
        if (square.isupper() and self.turn=="black") or (square.islower() and self.turn=="white"):
            return True
        else:
            return False
    
    def onRow(self,xStart,yStart,_,__nRow):
        if xStart==nRow:
            return True
        else:
            return False
    
    
    def moveAllowed(self,xStart,xFinish,yStart,yFinish,move):
        functionAnswers=[]
        for condition in move[0].split("+"):
            condition=condition.split("/")
            toExec=condition[0]+"(xStart,xFinish,yStart,yFinish"
            try: toExec+=condition[1]+")"
            except: toExec+=")"
            functionAnswers.append(exec(toExec))
        if False in functionAnswers:
            return False
        else:
            return True
    
    def movePiece(self,move):
        self.start,self.finish=move[:2],move[2:]
        self.xStart,self.yStart=self.chessToList(start)
        self.xFinish,self.yFinish=self.chessToList(finish)
        move=input("Move : ") # To implement in a better way
        if moveAllowed(move):
            self.chessboard[xFinish][yFinish]=self.chessboard[xStart][yStart]
            self.chessboard[xStart][yStart]="."
