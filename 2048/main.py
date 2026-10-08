from random import choice, sample
from copy import deepcopy #useful for 2+D arrays



def getEmptyTiles(grid: list[list[int]]) -> list[list[int,int]]:
    """
    get all empty tiles in a grid and returns their indexes
    """
    emptyTiles = []

    for i in range(len(grid)): #go through each row
        for j in range(len(grid[i])): #go through each tile
            #log 2D index of empty tiles
            if grid[i][j] == " ":
                emptyTiles.append([i,j])
    
    return emptyTiles


def removeEmptyTiles(grid: list[list[str]]) -> list[list[str]]:
    """
    removes empty tiles from a given grid
    """

    #creates a new 2D array without the empty tiles and returns it
    return [[tile for tile in row if tile != " "] for row in grid]


def fillGrid(
        grid: list[list[str]], 
        fillFront=False, 
        fillBack=False
        ) -> list[list[str]]:
    """
    will take a grid that is missing tiles and fill it with empty tiles to match a 4x4 grid size
    """

    #will default to fill back if fillFront and fillBack not set
    if fillFront:
        grid = [list(" "*(4-len(row))) + row for row in grid]
    elif not fillFront or fillBack:
        grid = [row + list(" "*(4-len(row))) for row in grid]

    return grid


def rotateGrid(grid: list[list[str]]) -> list[list[str]]:
    """
    rotates grid
    """
    
    #returns a new rotated grid based on amount of items on first row
    return [[row[i] for row in grid] for i in range(len(grid[0]))]


def spawnTile(grid: list[list[str]]):
    """
    function will create a tile in any blank parts of the grid given
    """

    #chance of spawning tiles (out of 10)
    probability = {
        "2": 9,
        "4": 1
    }

    #create a list of possible tiles to spawn based on probability
    possibleTiles = sample(
        list(probability.keys()), 
        counts=list(probability.values()), 
        k=10
        )
    
    #choose a tile to spawn and get all of the empty tiles
    tileChoice = choice(possibleTiles)
    emptyTiles = getEmptyTiles(grid)

    if emptyTiles: #will only spawn a tile if there is an empty tile
        x, y = choice(emptyTiles)
        grid[x][y] = tileChoice #update the grid


def mergeTiles(grid: list[list[str]], invert=False) -> int:
    """
    merge tiles that are next to each other if they are equal
    """
    mergeVal = 0 #score

    for row in grid:
        if not invert:
            for i in range(len(row)-1):
                if i+1 < len(row) and row[i] == row[i+1]: #will execute logic up to 2nd last tile
                    resultant = int(row[i]) + int(row[i+1]) #get the resulting combination of the two tiles
                    
                    #remove row[i] and row[i+1]
                    row.pop(i)
                    row.pop(i)

                    #insert the new resultant in their place
                    row.insert(i, str(resultant))

                    mergeVal += resultant
        elif invert:
            for i in reversed(range(1,len(row))):
                if row[i] == row[i-1]: #will execute logic up to 2nd first tile
                    resultant = int(row[i]) + int(row[i-1]) #get the resulting combination of the two tiles
                    
                    #remove row[i] and row[i-1]
                    row.pop(i)
                    row.pop(i-1)

                    #insert the new resultant in their place
                    row.insert(i-1, str(resultant))

                    mergeVal += resultant

    return mergeVal


def displayGrid(grid: list[list[str]]):
    """
    display grid in terminal
    """
    
    #tbh idk what to do
    for row in grid:
        print(row)


def move(
        grid: list[list[str]],
        move: str
        ) -> list[list[list[str]], int]:
    """
    move tiles horizontally or vertically based on given move
    """

    #move tiles
    if move in "ad": #handle horizontal movement
        tempGrid = removeEmptyTiles(grid) #remove empty tiles
        score = mergeTiles(tempGrid, invert= move=="d") #merge tiles next to each other if they are the same
        grid = fillGrid(tempGrid, fillFront= move=="d") #fill grid to be 4x4 size
    elif move in "ws": #handle vertical movement
        tempGrid = rotateGrid(grid) #rotate grid to focus on columns without reworking a lot of logic
        
        #same procedure as before
        tempGrid = removeEmptyTiles(tempGrid) 
        score = mergeTiles(tempGrid, invert= move=="s") 
        tempGrid = fillGrid(tempGrid, fillFront= move=="s")

        grid = rotateGrid(tempGrid) #rotate grid back in place so that if focuses on its rows again

    return grid, score


def getInput(customMsg="") -> str:
    """
    get wasd input from user
    """

    try:
        move = str(input(f"wasd{customMsg}: ")).lower() #get raw str input
    except Exception as e:
        getInput(customMsg=f" ({e})") #if any errors occur it will call itself and give itself its error msg
    else:
        #validate input and return it if valid
        if move in "wasd" and len(move)==1:
            return move
        else:
            getInput(customMsg=" (INVALID INPUT)") #if not valid it will call itself and tell itself to say input is invalid


def checkGameOver(grid: list[list[str]]) -> bool:
    gameOver = False

    if not getEmptyTiles(grid): #skip a bunch of logic if theres space in the board
        score1 = mergeTiles(deepcopy(grid)) #check horizontal movement

        #check vertical movement
        rGrid = rotateGrid(deepcopy(grid))
        score2 = mergeTiles(rGrid)

        #verify if any legal moves cannot be made
        if score1 == 0 and score2 == 0:
            gameOver = True

    return gameOver


def main():
    """
    main gameloop
    """

    grid = [
        [" ", " ", " ", " "],
        [" ", " ", " ", " "],
        [" ", " ", " ", " "],
        [" ", " ", " ", " "]
    ]
    prevGrid = []
    score = 0

    #beginning, spawn 2 tiles
    spawnTile(grid)

    #gameloop
    while True:
        #show player grid and score
        if grid != prevGrid: #if an input has been given and nothing has changed, it will not spawn a new tile
            spawnTile(grid)

        print(f"score: {score}")
        displayGrid(grid)
        
        if checkGameOver(grid): #stop mainloop and execute game over block
            break

        #get input, move tiles, add to score, and keep a reference to the grid in case input caused no tiles to move
        m = getInput()
        prevGrid = grid
        grid, s = move(grid, m)
        score += s

    print(f"GAME OVER\nFINAL SCORE: {score}") #tell player game over



if __name__ == "__main__": #makes tests with functions easier
    main()