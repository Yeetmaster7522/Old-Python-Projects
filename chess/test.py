from pieces import *
from player import Player as plyr
p = Piece([4,4])
s = plyr("white")
print(p.isPathObstructed([4,4], [5,3], s.getCoords().keys()))