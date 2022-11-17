import copy
import time

"""
Prints the entire board to the console, including current guesses.
"""
def printBoard(board):
    for j in range(9):
        for dj in range(3):
            print(" ",end="")
            for i in range(9):
                for di in range(3):
                    if type(board[j][i])==int:
                        if dj==1 and di==1:
                            print(board[j][i],end="")
                        else:
                            print(" ",end="")
                    elif dj*3+di+1 in board[j][i]:
                        print(dj*3+di+1,end="")
                    else:
                        print(" ",end="")
                    print(" ",end="")
                if (i+1)%3!=0:    
                    print("| ",end="")
                if (i+1)%3==0 and i!=8:
                    print("M ",end="")
            print()
        if (j+1)%3==0 and j != 8:
            print("N"*71)
        elif j!=8:
            line = (("-"*7+"|")*3)[:-1]+"M"
            for across in range(3):
                if across!=2:
                    print(line,end="")
                else:
                    print(line[:-1])
    print()
    print()
    print()

"""
Returns False if two boards are identical, True otherwise.
"""
def compare(board, oldBoard):
    for i in range(9):
        for j in range(9):
            if type(board[j][i]) != type(oldBoard[j][i]):
                return True
            if type(board[j][i]) != int:
                if len(board[j][i]) != len(oldBoard[j][i]):
                    return True
    return False

"""
Returns actual specified row from board.
"""
def getRowGuess(board,y):
    return board[y]

"""
Returns copy of specified row with 0s instead of guesses.
"""
def getRow(board,y):
    return [val if type(val)==int else 0 for val in getRowGuess(board,y)]

"""
Returns a copy of specified column from board with actual guess arrays.
"""
def getColGuess(board,x):
    return [row[x] for row in board]

"""
Returns copy of specified column with 0s instead of guesses.
"""
def getCol(board,x):
    return [val if type(val)==int else 0 for val in getColGuess(board,x)]

"""
Returns a copy of the 3x3 square containing position x,y from board with actual guess arrays.
"""
def getSquareSquare(board,y,x):
    out = [[0]*3 for i in range(3)]
    lowY = (y//3)*3
    lowX = (x//3)*3
    for dy in range(3):
        for dx in range(3):
            Y=dy+lowY
            X=dx+lowX
            out[dy][dx] = board[Y][X]
    return out

"""
Returns a copy of a 2-dimensional array as a 1-dimensional array with actual guess arrays.
"""
def squareToRow(square):
    out = []
    for row in square:
        out += row
    return out


"""
Returns a copy of the square containing x,y as a 1-dimensional array with 0s instead of guesses.
"""
def getSquare(board,y,x):
    out = squareToRow(getSquareSquare(board,y,x))
    for elem in out:
        if type(elem)!=int:
            elem=0
    return out

"""
Removes guesses from a position on the board if it exists in the same square, row or column as a set value.
"""
def checkSets(board,y,x):
    if type(board[y][x])==int:
        return
    for val in range(1,10):
        if val in board[y][x]:
            if val in getRow(board,y) or val in getCol(board,x) or val in getSquare(board,y,x):
                board[y][x].remove(val)

"""
Runs checkSets(board,y,x) for every position on the board.
"""
def checkBoardSets(board):
    for y in range(9):
        for x in range(9):
            checkSets(board,y,x)

"""
Sets values at every position if there is only one guess for that position. Returns True if there is an unset position with no guesses, False otherwise.
"""
def simplify(board):
    for y in range(9):
        for x in range(9):
            if type(board[y][x])!=int:
                if len(board[y][x])==1:
                    board[y][x]=board[y][x][0]
                elif len(board[y][x])==0:
                    return True
    return False

"""
Returns False if there is a row, column or square with two of the same set values, True otherwise.
"""
def isValid(board):
    for y in range(9):
        for x in range(9):
            if type(board[y][x])==int:
                if getRow(board,y).count(board[y][x]) > 1:
                    return False
                if getCol(board,x).count(board[y][x]) > 1:
                    return False
                if getSquare(board,y,x).count(board[y][x]) > 1:
                    return False
    return True

"""In the following two functions, square is the relevant coordinate of the square [0,3)"""
"""#####################################################################################"""
"""
Removes a guess from every unset position in a row if the position is not in the specified square.
"""
def removeFromRow(board,y,val,square):
    for i in range(9):
        elem = board[y][i]
        if i//3!=square and type(elem)!=int and val in elem:
            elem.remove(val)

"""
Removes a guess from every unset position in a row if the position is not in the specified square.
"""
def removeFromCol(board,x,val,square):
    for i in range(9):
        if i//3!=square and type(board[i][x])!=int and val in board[i][x]:
            board[i][x].remove(val)

"""
Removes values from positions outside of the square if the guesses for that value inside the square are in a line.
"""
def checkAlignments(board):
    for j in range(3):
        for i in range(3):
            squareSquare = getSquareSquare(board,3*j,3*i)
            for val in range(1,10):
                
                inRow = []
                for k in range(3):
                    row = squareSquare[k]
                    for elem in row:
                        if type(elem)!=int:
                            if val in elem:
                                inRow+=[k]
                                break
                                
                if len(inRow) == 1:
                    removeFromRow(board,3*j+inRow[0],val,i)
                    
                inCol = []
                for k in range(3):
                    col = []
                    for l in range(3):
                        col += [squareSquare[l][k]]
                    for elem in col:
                        if type(elem)!=int:
                            if val in elem:
                                inCol+=[k]
                                break
                
                if len(inCol) == 1:
                    removeFromCol(board,3*i+inCol[0],val,j)  

"""
Returns False if there is a difference between the values in two 2-dimensional arrays, True otherwise.
"""
def coordArrayEqual(arr1,arr2): #Currently not used.
    if len(arr1)!=len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i][0]!=arr2[i][0] or arr1[i][1]!=arr2[i][1]:
            return False
    return True

"""
Returns True if every coordinate pair in arr2 can be found within arr1, False otherwise.
"""
def coordArrayWithin(arr1,arr2):
    if len(arr1) == 0 or len(arr2) == 0:
        return False
    for i in range(len(arr2)):
        found = False
        for j in range(len(arr1)):
            if arr2[i][0] == arr1[j][0] and arr2[i][1] == arr1[j][1]:
                found = True
        if not found:
            return False
    return True

"""
Removes other guesses from groups of positions inside a square where there are enough guesses to fill the positions.
"""
def checkGroups(board):
    for squareY in range(3):
        for squareX in range(3):
            squareSquare = getSquareSquare(board,3*squareY,3*squareX)
            coords = [[] for i in range(9)]
            for val in range(1,10):
                for innerY in range(3):
                    for innerX in range(3):
                        elem = squareSquare[innerY][innerX]
                        if type(elem)!=int:
                            if val in elem:
                                coords[val-1]+=[[innerY,innerX]]
            for i in range(9):
                grouped = [i+1]
                for j in range(9):
                    if i!=j and coordArrayWithin(coords[i],coords[j]):
                        grouped += [j+1]
                if len(grouped) == len(coords[i]):
                    #remove other numbers
                    for member in range(len(coords[i])):
                        absoluteY = squareY*3+coords[i][member][0]
                        absoluteX = squareX*3+coords[i][member][1]
                        for guess in range(1,10):
                            if guess not in grouped and guess in board[absoluteY][absoluteX]:
                                board[absoluteY][absoluteX].remove(guess)

"""
Returns True if every element in the board is an integer and therfore set, False otherwise.
"""
def isComplete(board):
    for y in board:
        for x in y:
            if type(x)!=int:
                return False
    return True

"""
Returns a list of guesses from the given row that only appear once.
"""
def getAppearsOnce(row):
    found = []
    once = []
    for elem in row:
        if type(elem)!=int:
            for val in elem:
                if val not in found:
                    found += [val]
                    once += [val]
                elif val in once:
                    once.remove(val)
    return once

"""
Removes other guesses from every position on the board where this position is the only option for the guess in the row, square or column.
"""
def oneOption(board):
    sets = []
    for y in range(9):
        sets += [getRowGuess(board,y)]
    for x in range(9):
        sets += [getColGuess(board,x)]
    for y in range(3):
        for x in range(3):
            sets += [squareToRow(getSquareSquare(board,3*y,3*x))]
    for thisSet in sets:
        once = getAppearsOnce(thisSet)
        if len(once) == 0:
            continue
        for elem in thisSet:
            if type(elem)!=int:
                for solo in once:
                    if solo in elem:
                        for guess in elem:
                            if guess != solo:
                                elem.remove(guess)

"""
Converts an integer number of seconds into human readable string, assuming a year is 365 days long.
"""
def secondsToTime(seconds):
    lengths = [60,60,24,365]
    names = ["year","day","hour","minute","second"]
    count = [0,0,0,0,0]
    for i in range(len(lengths)):
        count[i] = seconds%lengths[i]
        seconds = int(seconds/lengths[i])
    count[-1] = seconds
    strings = []
    for i in range(len(count)):
        if count[-1-i] != 0:
            strings += [str(count[-1-i])+" "+names[i]+("s" if count[-1-i] != 1 else "")]
    return ', '.join(strings[:-1])+' and '+strings[-1] if len(strings) > 1 else strings[0]

"""
Tests every combination of guesses remaining for validity, copies to board and prints if there is one solution. If no solution or many solutions a message will be printed.
"""
def followPath(board):
    #print("No solution found with traditional methods")
    #print()
    print("Secret weapon unleashed")
    print()
    
    options = []
    paths = 1
    for y in range(9):
        for x in range(9):
            elem = board[y][x]
            if type(elem)!=int:
                options+=[len(elem)]
                paths*=len(elem)
    option = [0 for _ in range(len(options))]
    
    steps=50
    perc1="0%"
    perc2="100%"
    solutions = []
    start = time.time()
    estimated = False
    step = 0
    perc = 0
    
    for i in range(paths):
        
        if not estimated:
            if time.time() > start + 1:
                jump = i
                print(perc1+" "*(steps-len(perc1+perc2))+perc2+" "*3+"Attempts per second: "+str(jump)+" "*3+"Total time: "+secondsToTime(round(paths/jump)))
                estimated = True
        
        if estimated and (i==paths-1 or (i%jump)==0 or round(i*steps/paths)!=step or round(100*i/paths)!=perc):
            step = round(i*steps/paths)
            Si = str(round(i/jump))
            Spaths = str(round(paths/jump))
            perc = round(100*i/paths)
            Sperc = str(perc)
        
            #print("",end="\r")
            #time.sleep(1)
            print("M"*step+" "*(steps-step)+" "*3+(3-len(Sperc))*"0"+Sperc+"%"+" "*3+"0"*(len(Spaths)-len(Si))+Si+"/"+Spaths+" seconds",end="\r\r")
            #print("",end="")
        
        thisBoard = copy.deepcopy(board)
        selection=0
        for y in range(9):
            for x in range(9):
                if type(thisBoard[y][x])!=int:
                    thisBoard[y][x] = thisBoard[y][x][option[selection]]
                    selection+=1
        
        if isValid(thisBoard):
            solutions += [thisBoard]
        
        if i!=paths-1:
            option[0] += 1
            for j in range(len(options)):
                if option[j]==options[j]:
                    option[j]=0
                    option[j+1]+=1
    
    print()
    if len(solutions)>1:
        print("There are multiple solutions")
    elif len(solutions)==0:
        print("There are no solutions")
    else:
        for copyRow in range(9):
            board[copyRow] = solutions[0][copyRow]
    for solution in solutions:
        print()
        printBoard(solution)

"""
Returns True if every value in arr2 is in arr, and there is more than 1. False otherwise.
"""
def insideI(arr,arr2):
    for pos in arr2:
        if pos not in arr:
            return False
    for pos in arr2:
        if pos in arr:
            return True
    return False

"""
Removes other guesses from positions accross a row or column where there are enough guesses to fill the positions.
"""
def checkOptionLine(board):
    sets = []
    for xy in range(9):
        sets += [getRowGuess(board,xy)]
        sets += [getColGuess(board,xy)]
    for Set in sets:
        coords=[[] for _ in range(9)]
        for i in range(9):
            if type(Set[i])==int:
                continue
            for val in range(1,10):
                if val in Set[i]:
                    coords[val-1]+=[i]
        for val in range(1,10):
            grouped = [val]
            for val2 in range(1,10):
                if val!=val2:
                    if insideI(coords[val-1],coords[val2-1]):
                        grouped+=[val2]
            if len(grouped)>1 and len(grouped)>=len(coords[val-1]):
                for j in range(len(Set)):
                    if type(Set[j])!=int:
                        if val in Set[j]:
                            for guess in Set[j]:
                                if guess not in grouped:
                                    Set[j].remove(guess)

"""
Initializes the "2-dimensional" board from a 1 dimensional array of starting data. 0s represent gaps and are filled with arrays containing all potential guesses.
"""
def initBoard(board,entry):
    for i in range(len(entry)):
        if entry[i] == 0:
            entry[i] = [j for j in range(1,10)]
    
    for j in range(9):
        for i in range(9):
            board[j][i] = entry[j*9+i]


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():

    #medium
    entry = [0,1,2,9,0,8,4,0,7,0,0,0,0,7,0,8,2,5,0,7,5,0,0,0,0,0,1,0,0,0,5,0,0,0,0,6,4,0,3,0,9,1,7,8,0,9,0,7,4,8,0,0,1,0,0,0,8,2,6,9,1,0,0,7,0,0,0,0,0,0,6,9,1,9,6,0,0,0,0,0,0]
    #hard
    entry = [0,0,8,0,2,0,0,0,0,6,0,0,0,0,8,0,2,0,0,4,0,0,0,6,1,9,0,9,0,0,0,3,5,0,8,0,0,6,0,0,0,0,0,5,0,0,5,0,7,6,0,0,0,9,0,2,7,6,0,0,0,4,0,0,9,0,5,0,0,0,0,6,0,0,0,0,9,0,5,0,0]
    #hard with alignment
    entry = [5,9,0,0,0,0,0,0,3,0,0,1,3,9,0,0,0,6,8,0,0,5,0,6,9,1,7,0,0,0,0,0,0,0,0,1,0,1,0,0,0,7,5,8,9,0,4,0,8,0,9,7,0,0,0,0,0,0,0,3,6,9,0,0,0,0,9,4,5,0,7,8,7,5,9,0,0,0,1,3,0]
    #expert: 1 minute
    entry = [0,0,1,0,0,0,0,7,0,0,5,6,4,0,8,0,0,0,0,7,9,6,0,0,0,0,0,0,9,0,0,8,0,2,0,0,0,0,0,0,9,0,6,0,1,5,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,6,3,0,9,8,0,0,0,0,0,1,0,0,0]
    #expert: solveable
    #entry = [0,0,0,0,2,9,8,0,0,0,6,7,0,1,0,0,0,0,0,0,0,0,5,0,9,0,0,4,9,5,0,0,8,6,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,7,0,0,0,0,0,0,0,0,2,4,8,0,0,2,0,0,0,0,0,6,0,5,0,0,0,8,0,0,0,3]
    #extreme: 1 million years
    #entry = [0,2,0,0,0,0,0,7,0,0,0,0,5,0,0,0,6,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,3,5,0,0,0,1,0,0,7,0,0,0,0,0,0,0,0,0,0,9,0,8,9,0,5,0,0,0,4,0,0,6,0,0,0,2,0,0,0,0,0,0,0,8,0,0,0,0,0]
    #extreme: > age of universe
    #entry = [2,0,0,0,0,0,0,7,9,0,0,0,6,0,5,0,0,0,0,0,0,0,0,0,0,1,0,0,7,0,0,9,0,0,0,0,0,0,0,0,0,8,3,0,0,0,1,0,0,0,0,0,0,0,3,0,6,8,0,0,5,0,0,0,0,0,0,7,0,0,0,0,4,0,0,0,0,0,0,0,0]
    #extreme: > age of universe
    #entry = [1,0,0,0,6,0,0,7,0,7,0,8,0,0,0,0,0,0,4,0,0,2,0,0,0,0,0,3,0,0,0,0,4,0,0,0,0,6,0,0,0,0,0,9,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,4,0,8,0,5,0,0,9,0,0,0,0,0,0,0,0,0,0,6,0,0]
    #extreme: 1 day, 5 hours
    #entry = [7,0,0,0,2,8,0,0,9,4,0,0,0,0,6,0,3,0,0,0,0,0,5,0,0,0,0,0,5,2,0,0,0,8,0,0,0,0,0,3,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,9,0,0,0,0,0,0,0,0]
    
    
    board = [[0]*9 for i in range(9)]
    
    initBoard(board,entry)
    
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    different = True
    #complete = False
    
    while different:
        
        #simplify before print to show results of previous turn
        if (simplify(board)):
            printBoard(board)
            print("Ran out of options")
            break
        #simplify returns True if all options have been removed
        printBoard(board)
        
        if not isValid(board):
            print("Invalid")
            break
        
        oldBoard = copy.deepcopy(board)
        
        #time.sleep(5)
        time.sleep(0.2)
            
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        """ 1 """
        checkBoardSets(board)
        different = compare(board,oldBoard)
        if (different):
            print("Elimination")
            print()
            continue
        
        """ 2 """
        oneOption(board)
        different = compare(board,oldBoard)
        if (different):
            print("It is all I have")
            print()
            continue
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        
        
        checkOptionLine(board)
        
        different = compare(board,oldBoard)
        if (different):
            print("Cut out")
            print()
            continue
        
        
        checkGroups(board)
        
        different = compare(board,oldBoard)
        if (different):
            print("No room for possibilities")
            print()
            continue
        
        
        checkAlignments(board)
        
        different = compare(board,oldBoard)
        if (different):
            print("Alignment gun")
            print()
            continue
        
        
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        followPath(board)
        
        different = compare(board,oldBoard)
        if (different):
            print("Dr Strange")
            print()
            break
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        different = compare(board,oldBoard)
        
        #print(" " + ("Data changed" if different else "No progress found"))
    
    if isComplete(board):
        print("Too easy! WIN")
    else:
        print("Oh no! FAIL")
    
    time.sleep(10)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == "__main__":
    main()