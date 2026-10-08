"""
TASKS:
implement .isPathObstructed
make checkmate checks and implement stopping game if a checkmate is found
"""

#import classes and modules
from player import Player as plyr
from pieces import Piece
from json import load
from os import system, name

p = Piece([4,4]) #used for a couple of functions

def createGrid(white: plyr, black: plyr) -> dict[str, dict[str,str]]:
    #open up the default grid (used so default grid can be changed with minimal effort)
    with open("chess\\grid.json", "r") as f:
        grid = load(f)
    
    #populate grid with white and black pieces
    for piece in white.pieces:
        #get location of each piece and adds it to the grid with a str icon
        loc = white.pieces[piece].boardLoc()
        grid[loc[0]][loc[1]] = white.pieces[piece].icons[white.colour]
    
    for piece in black.pieces:
        #get location of each piece and adds it to the grid with a str icon
        loc = black.pieces[piece].boardLoc()
        grid[loc[0]][loc[1]] = black.pieces[piece].icons[black.colour]

    return grid

def displayBoard(grid: dict[str, dict[str,str]]):
    """
    prints out a grid
    """
    
    files = "    a   b   c   d   e   f   g   h\n"
    border = "  +---+---+---+---+---+---+---+---+\n"
    board = files + border

    # Loop through ranks (8 to 1) to build each row
    for rank in range(8, 0, -1):
        row = f"{rank} |"
        for file in "abcdefgh":
            piece = grid[file][str(rank)]
            row += f" {piece} |"
        board += row + "\n" + border

    print(board) #display grid in terminal

def getMove(turn) -> tuple[str, str]:
    """
    gets input from user
    """
    
    try:
        userInp = str(input(f"{"white's" if turn%2!=0 else "black's"} move (p1 p2): "))
    except ValueError:
        userInp = ""
    finally:
        return userInp.split()

def userMove(whitePlyr:plyr, blackPlyr:plyr, turn: int):
    """
    keeps asking user for inputs until a valid one is given and a piece is successfully moved\n
    |------------------------------------------------------------------------------------------|\n
    after moving, it will try to eat a piece
    """
    
    validInp = False #set loop up

    while not validInp:
        userInp = getMove(turn) #get moves
        if len(userInp) == 2: #check if two coords were given
            start, end = p.rawLoc(userInp[0]), p.rawLoc(userInp[1]) #get start and end pos
        elif userInp == ["concede"]:
            validInp = True
            continue
        else:
            continue #if two coords weren't given, then it will skip the rest of the code and go back to the beginnning
        
        #get positions of pieces from white and black players
        positionsW = whitePlyr.getCoords()
        positionsB = blackPlyr.getCoords()

        #check if a piece is at start position specified (depends on who's turn it is)
        if turn%2 != 0 and start in positionsW:
            piece = positionsW[start]
        elif turn%2 == 0 and start in positionsB:
            piece = positionsB[start]
        else:
            continue #if no piece was found to have the start pos, then it will skip the rest of the code and go back to the beginning

        #try to move the pieces
        #if the piece is unsuccessfully moved then it will continue looping
        if turn%2 != 0:
            if "pawn" in piece and whitePlyr.pieces[piece].move(end, whitePlyr.direction):
                validInp = True
            elif "pawn" not in piece and whitePlyr.pieces[piece].move(end):
                validInp = True
        else:
            if "pawn" in piece and blackPlyr.pieces[piece].move(end, blackPlyr.direction):
                validInp = True
            elif "pawn" not in piece and blackPlyr.pieces[piece].move(end):
                validInp = True

    if userInp == ["concede"]:
        return "end"
    else:
        #piece eating
        if end in positionsB and turn%2 != 0:
            blackPlyr.pieces.pop(positionsB[end])
        elif end in positionsW and turn%2 == 0:
            whitePlyr.pieces.pop(positionsW[end])
        return "continue"


def main():
    """
    mainloop
    """
    
    #init both players
    whitePlyr = plyr("white")
    blackPlyr = plyr("black")

    #set up some stuff for the game
    checkmate = False
    turn = 0

    #gameloop keeps going until checkmate is achieved
    while not checkmate:
        turn += 1 #increment turn counter
        system('cls' if name == 'nt' else 'clear') #reset terminal, works on windows and unix systems
        displayBoard(createGrid(whitePlyr, blackPlyr)) #display the chessboard

        move = userMove(whitePlyr, blackPlyr, turn) #get user input
        if move == "end":
            checkmate = True
        print() #adds a space between each move (mainly used for debugging when terminal not cleared)

    #clear terminal and announce winnner
    system('cls' if name == 'nt' else 'clear')
    print(
        f"""
|--------------------------|

    |   {"WHITE" if turn%2==0 else "BLACK"} WON!!!   |

|--------------------------|
        """
          )

main()