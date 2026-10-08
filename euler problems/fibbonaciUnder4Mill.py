rawNum = []
currentNum = 1

while True:
    currentNum += currentNum
    if currentNum >= 4000000:
        break

    rawNum.append(currentNum)

evenNum = [n for n in rawNum if n % 2 == 0]
print(sum(evenNum))