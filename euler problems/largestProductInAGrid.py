import math

f = open("euler problems\\grid.txt", "r")
grid = []
products = []

for line in f:
    line = line.split()
    grid.append(list(map(int, line)))

#left/right products
for x in range(len(grid)):
    for y in range(x-4):
        items = grid[x][y:y+4]
        products.append(math.prod(items))

#up/down products
for x in range(len(grid)): #-4
    for y in range(x):
        items = []
        for row in grid[x:x+4]:
            items.append(row[y])
        print(items)
        products.append(math.prod(items))

#diagonal products
for x in range(len(grid)): #-4
    for y in range(x): #-4
        items = []
        counter = 0
        for row in grid[x:x+4]:
            items.append(row[y+counter])
            counter += 1
        products.append(math.prod(items))

products = sorted(products)
print(products)
print(products[-1])