"""
all of the classes for the program

methods:
.firstMove bool
.icons str
.coord = list
.move() moves piece to new location with verification if it is valid
.boardLoc() board location
.rawLoc() turns board location into format used by .coord
"""

class Piece:
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """
    
    def __init__(self, coord: tuple): #init base class
        self.col = "abcdefgh" #columns on the chessboard
        self.moves = () #default of possible relative positions a piece can move to
        self.firstMove = True #default if first move of the piece (useful for pawns)
        self.icons = "֍֍" #default icons for pieces, i=0 is black, i=1 is white

        #check to see if coordinate is valid and raise an error if it is not
        if self.validate(coord):
            self.coord = coord
        else:
            raise ValueError("Coordinate does not exist")
    
    def move(self, destination: tuple, moveset: tuple, direction=0, checkPath=True) -> bool:
        """
        change coord to destination if valid and returns if it has moved to the destination successfully
        """

        moved = False

        #goes through every relative move piece can make and checks if the destination is equal to the absolute coord
        for move in moveset:
            newCoord = (self.coord[0]+move[0], self.coord[1]+move[1]) #create an absolute pos for validation
            if destination == newCoord and self.validate(newCoord):
                if direction == 0:
                    #update coordinate and moved
                    self.coord = newCoord
                    moved = True
                elif direction == 1 and newCoord[1] >= self.coord[1]:
                    self.coord = newCoord
                    moved = True
                elif direction == -1 and newCoord[1] <= self.coord[1]:
                    self.coord = newCoord
                    moved = True

        return moved
    
    def validate(self, coord: tuple) -> bool:
        """
        returns true if the given coord is valid
        """
        
        return coord[0] <= len(self.col) and coord[1] <= 8 and coord[0] >= 0 and coord[1] > 0
    
    def boardLoc(self) -> str:
        """
        returns a chessboard coord based on the piece's raw coord\n
        e.g. c4
        """
        
        return f"{self.col[self.coord[0]]}{self.coord[1]}"
    
    def rawLoc(self, coord: str) -> tuple[int, int]:
        """
        returns raw location based on chessboard coord\n
        e.g. [col, row]
        """

        try:
            coord = (self.col.index(coord[0]), int(coord[1]))
        except Exception as e: #catch any errors in creating a raw location from an input and outputs an empty tuple if the input is invalid
            coord = ()
            print(e)
        finally:
            return coord
        
    def isPathObstructed(self, start: tuple[int,int], end: tuple[int,int], positions: list[tuple[int,int]]) -> bool:
        direction = [(n>0)-(n<0) for n in (end[0]-start[0], end[1]-start[1])]
        current = start

        while current != end:
            current[0] += direction[0]
            current[1] += direction[1]

            if tuple(current) in positions:
                return True
            
        return False

class Pawn(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """

    def __init__(self, coord: tuple):
        super().__init__(coord) #initialise stuff from parent class
        
        self.moves = ( #list of possible relative positions a pawn can move to
            (0,1),
            (1,1),
            (-1,1),
            (0,-1),
            (1,-1),
            (-1,-1),
        )
        self.icons = "♙♟" #str of icons the pawn uses

    def move(self, destination: tuple, direction: int):
        """
        based off of Piece.move() but adds pawn specific logic
        """
        
        #adds moves that a pawn can do when its it's first turn
        if self.firstMove:
            moveset = self.moves + tuple([(0,2)]) + tuple([(0,-2)])
        else:
            moveset = self.moves
        
        moved = super().move(destination, moveset, direction=direction)
        if moved: #call parent class .move() function
            self.firstMove = False
        return moved

class Knight(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """

    def __init__(self, coord: tuple):
        super().__init__(coord)

        self.moves = ( #list of possible relative positions a knight can move to
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
        )
        self.icons = "♘♞" #str of icons the knight uses

    def move(self, destination: tuple):
        return super().move(destination, self.moves) #call parent class .move() function
    
class Bishop(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """

    def __init__(self, coord: tuple):
        super().__init__(coord)

        self.moves = ( #list of possible relative positions a bishop can move to
            ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7))
        )
        self.icons = "♗♝" #str of icons the bishop uses

    def move(self, destination: tuple):
        return super().move(destination, self.moves) #call parent class .move() function
    
class Rook(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """

    def __init__(self, coord):
        super().__init__(coord)

        self.moves = ( #list of possible relative positions a rook can move to
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7))
        )
        self.icons = "♖♜" #str of icons the rook uses

    def move(self, destination: tuple):
        return super().move(destination, self.moves) #call parent class .move() function
    
class Queen(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """
    
    def __init__(self, coord):
        super().__init__(coord)

        self.moves = ( #list of possible relative positions a queen can move to
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7))
        )
        self.icons = "♕♛" #str of icons the queen uses

    def move(self, destination: tuple):
        return super().move(destination, self.moves) #call parent class .move() function

class King(Piece):
    """
    includes these methods:\n
    \t- self.firstMove #bool
    \t- self.icons #str
    \t- self.coord #list
    \t- self.move() #moves piece to new location with verification if it is valid
    \t- self.boardLoc() #board location
    \t- self.rawLoc() #turns board location into format used by .coord
    """
    
    def __init__(self, coord):
        super().__init__(coord)

        self.moves = ( #list of possible relative positions a king can move to
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        )
        self.icons = "♔♚" #str of icons the king uses

    def move(self, destination: tuple):
        return super().move(destination, self.moves) #call parent class .move() function


#debugging and testing
if __name__ == "__main__":
    pass