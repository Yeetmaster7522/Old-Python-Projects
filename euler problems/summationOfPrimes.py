n = 2000000
numL = {x: True for x in list(range(2,n)) if x % 2 != 0 or x == 2}
p = 3

while p**2 < n:
    print(f"checking {p}")
    for x in range(p, n):
        if p*x in numL:
            numL[p*x] = False
        else:
            break
    p += 2

primeNum = [key for key in numL if numL[key]]
print(primeNum)
print(sum(primeNum))