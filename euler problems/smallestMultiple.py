pMultiples = [1, 2, 3, 5, 7, 11, 13, 17, 19]
found = False
number = 19

while True:
    output = [number%n for n in pMultiples]
    #print(f"{number}: {output}")
    if len(set(output)) == 1:
        break
    else:
        number += 19

print(number)