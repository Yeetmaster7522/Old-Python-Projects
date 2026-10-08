from pieces import *

class Player:
    """
    self.colour = 0 #black\n
    self.colour = 1 #white\n
    self.pieces = {piece, piece, ...} #each piece has the following methods:\n
    \t- self.pieces[piece].firstMove #bool
    \t- self.pieces[piece].icons #str
    \t- self.pieces[piece].coord #list
    \t- self.pieces[piece].move() #moves piece to new location with verification if it is valid
    \t- self.pieces[piece].boardLoc() #board location
    \t- self.pieces[piece].rawLoc() #turns board location into format used by .coord
    """
    def __init__(self, colour: str):
        #generates things differently based on colour
        if colour == "black":
            self.colour = 0
            pawnRow = 7
            kingRow = 8
            self.direction = -1
        elif colour == "white":
            self.colour = 1
            pawnRow = 2
            kingRow = 1
            self.direction = 1
        
        #list of all the pieces a player has
        self.pieces = {
            "pawn1": Pawn(coord=(0,pawnRow)),
            "pawn2": Pawn(coord=(1,pawnRow)),
            "pawn3": Pawn(coord=(2,pawnRow)),
            "pawn4": Pawn(coord=(3,pawnRow)),
            "pawn5": Pawn(coord=(4,pawnRow)),
            "pawn6": Pawn(coord=(5,pawnRow)),
            "pawn7": Pawn(coord=(6,pawnRow)),
            "pawn8": Pawn(coord=(7,pawnRow)),
            
            "rook1": Rook(coord=(0,kingRow)),
            "rook2": Rook(coord=(7,kingRow)),
            
            "knight1": Knight(coord=(1,kingRow)),
            "knight2": Knight(coord=(6,kingRow)),
            
            "bishop1": Bishop(coord=(2,kingRow)),
            "bishop2": Bishop(coord=(5,kingRow)),

            "king": King(coord=(4,kingRow)),
            "queen": Queen(coord=(3,kingRow))
        }

    def getCoords(self) -> dict[tuple[int,int], str]:
        """
        returns a dict containing the pieces and their coords\n
        {
            (x,y): piece
        }
        """

        coords = {}
        for piece in self.pieces:
            coords[self.pieces[piece].coord] = piece
        return coords