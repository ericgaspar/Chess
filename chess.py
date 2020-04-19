chessboard=[["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]]
turn="white"
end=False
possibleMoves={"k":[["noCheck",x,y] for x in range(-1,2) for y in range(-1,2) if [x,y]!=[0,0]]+[["canCastle/kingside",0,2],["canCastle/queenside",0,-2]],
               "q":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==y or x==0 or y==0) and [x,y]!=[0,0]],
               "r":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if (x==0 or y==0) and [x,y]!=[0,0]],
               "b":[["notTeammate+noPieceBetween",x,y] for x in range(-7,8) for y in range(-7,8) if x==y!=0],
               "n":[["notTeammate",x,y] for [x,y] in [[-2,-1],[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2]]],
               "p":[["notTeammate+isWhite",-1,0],["notTeammate+noPieceBetween+onRow/2+isWhite",-2,0],["enemyOrEnPassant+isWhite",-1,-1],["enemyOrEnPassant+isWhite",-1,1],
                    ["notTeammate+isBlack",1,0],["notTeammate+noPieceBetween+onRow/7+isBlack",2,0],["enemyOrEnPassant+isBlack",1,-1],["enemyOrEnPassant+isBlack",1,1]]}

def chessToList(coord):
    x=8-int(coord[1])
    y=ord(coord[0])-97
    return x,y


def noCheck(xStart,yStart,_,__):
    global chessboard,possibleMoves
    check=False
    for x in range(8):
        for y in range(8):
            square=chessboard[x][y]
            if square!=".":
                for move in possibleMoves[square.lower()]:
                    if moveAllowed(move) and x+move[1]==xStart and y+move[2]==yStart:
                        return False
    return True

def notTeammate(_,__,xFinish,yFinish):
    global chessboard,turn
    square=chessboard[xFinish][yFinish]
    if (square.isupper() and turn=="white") or (square.islower() and turn=="black"):
        return False
    return True

def noPieceBetween(xStart,yStart,xFinish,yFinish):
    global chessboard
    if xStart==xFinish: # horizontal
        if yStart<yFinish and chessboard[xStart][yStart+1:yFinish]==["."]*(yFinish-yStart+1):
            return True
        elif yFinish<yStart and chessboard[xStart][yFinish+1:yStart]==["."]*(yStart-yFinish+1):
            return True
        return False
    elif yStart==yFinish: # vertical
        if xStart<xFinish:
            squareStripe=range(xStart+1,xFinish)
        else:
            squareStripe=range(xFinish+1,xStart)
        for x in squareStripe:
            if chessboard[x][yStart]!=".":
                return False
        return True
    else: # diagonal
        if xStart>xFinish:
            for diff in range(xStart-xFinish+1):
                if chessboard[xFinish+diff][yFinish+diff]!=".":
                    return False
        else:
            for diff in range(xFinish-xStart+1):
                if chessboard[xStart+diff][yStart+diff]!=".":
                    return False
        return True

def enemyOrEnPassant(_,__,xFinish,yFinish):
    global chessboard,turn
    square=chessboard[xFinish][yFinish]
    if (square.isupper() and turn=="black") or (square.islower() and turn=="white"):
        return True
    return False

def onRow(xStart,yStart,_,__,nRow):
    if 8-xStart==nRow:
        return True
    return False

def isWhite(xStart,yStart,_,__):
    global chessboard
    if chessboard[xStart][yStart].isupper():
        return True
    return False

def isBlack(xStart,yStart,_,__):
    global chessboard
    if chessboard[xStart][yStart].islower():
        return True
    return False

def canCastle(xStart,yStart,_,__,side):
    return False


def moveAllowed(xStart,yStart,xFinish,yFinish,piece):
    global turn
    warning="Warning, your move isn't correct!"
    if (piece.isupper() and turn=="black") or (piece.islower() and turn=="white"):
        print(warning)
        return False
    for square in [xStart,yStart,xFinish,yFinish]:
        if square<0 or square>7:
            print(warning)
            return False
    xDiff,yDiff=xFinish-xStart,yFinish-yStart
    
    foundMove=False
    for moveTest in possibleMoves[piece.lower()]:
        if [moveTest[1],moveTest[2]]==[xDiff,yDiff]:
            move=moveTest
            foundMove=True
            break
    if not foundMove:
        print(warning)
        return False
      
    functionAnswers=[]
    for condition in move[0].split("+"):
        condition=condition.split("/")
        toExec=""+condition[0]+"(xStart,yStart,xFinish,yFinish"
        try: toExec+=","+condition[1]+")"
        except: toExec+=")"
        functionAnswers.append(eval(toExec))
    if False in functionAnswers:
        print(warning)
        return False
    return True

def movePiece():
    global chessboard,turn
    print()
    for ligne in chessboard:
        print("".join(ligne))
    print()
    move=input("Move : ")
    start,finish=move[:2],move[2:]
    xStart,yStart=chessToList(start)
    xFinish,yFinish=chessToList(finish)
    piece=chessboard[xStart][yStart]
    if moveAllowed(xStart,yStart,xFinish,yFinish,piece):
        chessboard[xFinish][yFinish]=piece
        chessboard[xStart][yStart]="."
        if turn=="white":
            turn="black"
        else:
            turn="white"

while True:
    movePiece()
