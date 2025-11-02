import math
import random

def circle_square_mk(r, n):
    if r < 0 or n < 0:
        return 'Error'
    k = 0
    for i in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x ** 2 + y ** 2 <= r ** 2:
            k += 1
    return ((k / n) * (4 * r ** 2))

if __name__ == "__main__":
    r, n = map(int, input().split())
    print(circle_square_mk(r, n))
    print(math.pi * r ** 2)
    #При входных значения r = 2 и n = 1000 площадь, вычисленная методом Монте-Карло, имеет погрешность около 0.08
    #При входных значения r = 2 и n = 10000 площадь, вычисленная методом Монте-Карло, имеет погрешность около 0.01
    #Таким образом можно сделать вывод, что при увеличении кол-ва экспериментов, точность расчёта повышается