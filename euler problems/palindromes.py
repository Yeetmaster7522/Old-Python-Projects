#find largest palindrome made from the product of two 3 digit numbers
#largest number possible is 6 digits

numList = []

for x in reversed(range(100, 999)):
    for y in reversed(range(100, 999)):
        number = str(x * y)
        if number[:3] == number[:-4:-1]:
            numList.append(int(number))

numList.sort(reverse=True)
print(numList[0])