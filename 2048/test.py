from main import move

grid = [
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '2'],
    ['2', '2', '2', '4']
]

grid, score = move(grid, "d")
print(grid)
