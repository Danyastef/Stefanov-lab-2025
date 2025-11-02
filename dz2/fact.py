import time

def fact_rec(n):
    if 1 <= n <= 10**5:
        if n == 1:
            return 1
        return n * fact_rec(n-1)
    else:
        return 'Error'

def fact_it(n):
    if 1 <= n <= 10**5:
        factorial = 1
        for i in range(2, n+1):
            factorial *= i
        return factorial
    else:
        return 'Error'

def func_time(func, n):
    start = time.time()
    func(n)
    end = time.time()
    return end - start

if __name__ == '__main__':
    n = 0
    it_time = func_time(fact_it, n)
    rec_time = func_time(fact_rec, n)
    print(f'Скорость работы рекурсивной функции: {rec_time} секунд')
    print(f'Скорость работы итерационной функции: {it_time} секунд')

# Скорость работы итерационной функции меньше, чем рекурсивной.
# Разница во времени увеличивается с ростом n.