n = int(input())
if 1 <= n <= 20:
    a = 0
    for i in range(1,n+1):
        if i < 10:
            a = a*10 + i
        else:
            a = a*100 + i
    print(a)
else:
    print("Error")