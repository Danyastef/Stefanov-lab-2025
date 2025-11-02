cube = lambda x: x**3

def fibonacci(n):
    if not 1 <= n <= 15:
        return 'Error'
    fib_nums = [0, 1]
    if n == 1:
        return [0]
    for i in range(2, n):
        fib_nums.append(fib_nums[i-1]+fib_nums[i-2])
    return fib_nums

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))