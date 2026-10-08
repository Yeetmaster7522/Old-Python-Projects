limit = 999

for m in range(2, limit):
    for n in range(1, m-1):
        a = m**2 - n**2
        b = 2*n*m
        c = n**2 + m**2
        if a+b+c == 1000:
            print(f"{a}:{b}:{c}")
            print(a*b*c)