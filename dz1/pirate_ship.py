n, m = map(int, input().split())
if n > 0 and m > 0:
    cargo = []
    for i in range(m):
        name, weight, cost = input().split()
        if int(weight) <= 0 or int(cost) <= 0:
            print('Error')
            exit()
        cargo.append([name, int(weight), int(cost)])
    result = []
    for c in cargo:
        c.append(c[2] / c[1])
    cargo = sorted(cargo, key=lambda cargo_value: cargo_value[3], reverse=True)
    for c in cargo:
        name = c[0]
        weight = c[1]
        cost = c[2]
        if weight <= n:
            result.append([name, weight, cost])
            n -= weight
        else:
            result.append([name, round(n, 2), round(cost * n / weight, 2)])
            break
    for i in sorted(result, key=lambda cost: cost[2], reverse=True):
        print(i[0], i[1], i[2])
else:
    print('Error')