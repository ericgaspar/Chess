board = [["r", "n", "b", "q", "k", "b", "n", "r"],
         ["p", "p", "p", "p", "p", "p", "p", "p"],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         ["P", "P", "P", "P", "P", "P", "P", "P"],
         ["R", "N", "B", "Q", "K", "B", "N", "R"]]
turn = "white"
end = False
possibleMoves = {"k": [["noCheck", x, y] for x in range(-1, 2) for y in range(-1, 2) if [x, y] != [0, 0]] + [["canCastle/kingside", 0, 2], ["canCastle/queenside", 0, -2]],
                 "q": [["notTeammate+noPieceBetween", x, y] for x in range(-7, 8) for y in range(-7, 8) if (x == y or x == 0 or y == 0) and [x, y] != [0, 0]],
                 "r": [["notTeammate+noPieceBetween", x, y] for x in range(-7, 8) for y in range(-7, 8) if (x == 0 or y == 0) and [x, y] != [0, 0]],
                 "b": [["notTeammate+noPieceBetween", x, y] for x in range(-7, 8) for y in range(-7, 8) if abs(x) == abs(y) != 0],
                 "n": [["notTeammate", x, y] for [x, y] in [[-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]],
                 "p": [["notTeammate+isWhite", -1, 0], ["notTeammate+noPieceBetween+onRow/2+isWhite", -2, 0], ["enemyOrEnPassant+isWhite", -1, -1], ["enemyOrEnPassant+isWhite", -1, 1],
                       ["notTeammate+isBlack", 1, 0], ["notTeammate+noPieceBetween+onRow/7+isBlack", 2, 0], ["enemyOrEnPassant+isBlack", 1, -1], ["enemyOrEnPassant+isBlack", 1, 1]]}
whiteKing = [7, 4]
blackKing = [0, 4]

def chessToList(coord):
    x = 8 - int(coord[1])
    y = ord(coord[0]) - 97
    return x, y


def noCheck(_, __, xKing, yKing):
    return not isCheck(xKing, yKing)

def isCheck(xKing, yKing):
    global board, possibleMoves
    check = False
    for x in range(8):
        for y in range(8):
            square = board[x][y]
            if square != ".":
                for move in possibleMoves[square.lower()]:
                    if moveAllowed(x, y, xKing, yKing, square) and x + move[1] == xKing and y + move[2] == yKing:
                        return True
    return False

def notTeammate(_, __, xFinish, yFinish):
    global board, turn
    square = board[xFinish][yFinish]
    if (square.isupper() and turn == "white") or (square.islower() and turn == "black"):
        return False
    return True

def noPieceBetween(xStart, yStart, xFinish, yFinish):
    global board
    if xStart == xFinish:  # horizontal
        if yStart < yFinish and board[xStart][yStart + 1:yFinish] == ["."] * (yFinish - yStart - 1):
            return True
        elif yFinish < yStart and board[xStart][yFinish + 1:yStart] == ["."] * (yStart - yFinish - 1):
            return True
        return False
    
    elif yStart == yFinish:  # vertical
        if xStart < xFinish:
            squareStripe = range(xStart + 1, xFinish)
        else:
            squareStripe = range(xFinish + 1, xStart)
        for x in squareStripe:
            if board[x][yStart] != ".":
                return False
        return True
    
    else:
        if xStart > xFinish:
            xSmallest = xFinish
        else:
            xSmallest = xStart
        if yStart > yFinish:
            ySmallest = yFinish
        else:
            ySmallest = yStart
        for diff in range(1, abs(xStart - xFinish)):
            if board[xSmallest + diff][ySmallest + diff] != ".":
                return False
        return True

def enemyOrEnPassant(_, __, xFinish, yFinish):
    global board, turn
    square = board[xFinish][yFinish]
    if (square.isupper() and turn == "black") or (square.islower() and turn == "white"):
        return True
    return False

def onRow(xStart, yStart, _, __, nRow):
    if 8 - xStart == nRow:
        return True
    return False

def isWhite(xStart, yStart, _, __):
    global board
    if board[xStart][yStart].isupper():
        return True
    return False

def isBlack(xStart, yStart, _, __):
    global board
    if board[xStart][yStart].islower():
        return True
    return False

def canCastle(xStart, yStart, _, __, side):
    return False


def moveAllowed(xStart, yStart, xFinish, yFinish, pieceMoving, pieceEaten):
    global turn
    if (pieceMoving.isupper() and turn == "black") or (pieceMoving.islower() and turn == "white"):
        return False
    for coord in [xStart, yStart, xFinish, yFinish]:
        if coord < 0 or coord > 7:
            return False
    if board[xStart][yStart] == ".":
        return False
    
    xDiff, yDiff = xFinish - xStart, yFinish - yStart
    foundMove = False
    for moveTest in possibleMoves[pieceMoving.lower()]:
        if moveTest[1] == xDiff and moveTest[2] == yDiff:
            move = moveTest
            foundMove = True
            break
    if not foundMove:
        return False
    
    functionAnswers = []
    for condition in move[0].split("+"):
        condition = condition.split("/")
        toExec = "" + condition[0] + "(xStart,yStart,xFinish,yFinish"
        try:
            toExec += "," + condition[1] + ")"
        except:
            toExec += ")"
        functionAnswers.append(eval(toExec))
    if False in functionAnswers:
        return False
    
    makeMove(xStart, yStart, xFinish, yFinish, pieceMoving)
    if check(whiteKing[0], whiteKing[1]) and turn=="black":
        whiteKingCheck=True
    elif check(blackKing[0], blackKing[1]) and turn=="white":
        blackKingCheck=True
    elif (check(whiteKing[0], whiteKing[1]) and turn=="white") or (check(blackKing[0], blackKing[1]) and turn=="black"):
        wrong=True
    undoMove(xStart, yStart, xFinish, yFinish, pieceMoving, pieceEaten)
    if wrong:
        return False
    
    if (pieceMoving!="R" and whiteKingCheck) or (pieceMoving!="r" and blackKingCheck):
        return False
    
    return True

def makeMove(xStart, yStart, xFinish, yFinish, pieceMoving):
    board[xStart][yStart] = "."
    board[xFinish][yFinish] = pieceMoving

def undoMove(xStart, yStart, xFinish, yFinish, pieceMoving, pieceEaten):
    board[xStart][yStart] = pieceMoving
    board[xFinish][yFinish] = pieceEaten
    

while True:
    print()
    for row in board:
        print("".join(row))
    print()
    move = input("Move : ")
    start, finish = move[:2], move[2:]
    xStart, yStart = chessToList(start)
    xFinish, yFinish = chessToList(finish)
    pieceMoving = board[xStart][yStart]
    pieceEaten = board[xFinish][yFinish]
    if moveAllowed(xStart, yStart, xFinish, yFinish, pieceMoving, pieceEaten):
        makeMove(xStart, yStart, xFinish, yFinish, pieceMoving)
        if turn == "white":
            turn = "black"
        else:
            turn = "white"
    else:
        print("Your move isn't correct!")
