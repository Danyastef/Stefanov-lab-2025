n = int(input())
if n > 0:
    times = []
    for i in range(n):
        a, b = map(int, input().split())
        if (a < b):
            times.append((a, b))
        else:
            print("Error")
            exit()
    t = int(input())
    if t > 0:
        pas_count = 0
        for a, b in times:
            if a <= t <= b:
                pas_count += 1
        print(pas_count)
    else:
        print("Error")
else:
    print("Error")