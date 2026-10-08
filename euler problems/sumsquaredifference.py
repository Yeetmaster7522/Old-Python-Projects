squareSum = sum([x**2 for x in range(1,101)])
sumSquare = sum(x for x in range(1,101))**2

print(sumSquare-squareSum)