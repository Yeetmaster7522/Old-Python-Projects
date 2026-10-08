#number 600851475143
#division tree https://byjus.com/maths/prime-factorization/#:~:text=The%20simplest%20algorithm%20to%20find,it%20cannot%20be%20further%20factorized.
primeNums = open("euler problems\\primes-to-100k.txt", "r")

factorTree = []
primeNums = [int(l.replace("\n", "")) for l in primeNums]

num = 600851475143

while num != 1.0:
    counter = 0
    for n in primeNums:
        if num % n == 0:
            num = num / n
            factorTree.append(num)
            break
        else:
            counter += 1
    print(factorTree)

print(factorTree[-2])