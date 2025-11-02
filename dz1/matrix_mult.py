n = int(input())
if 2 <= n <= 10:
    A = []
    B = []
    matr_multiply = [[0]*n for i in range(n)]
    for i in range(n):
        row = list(map(int, input().split()))
        if len(row) != n:
            print('Error')
            exit()
        A.append(row)
    for i in range(n):
        row = list(map(int, input().split()))
        if len(row) != n:
            print('Error')
            exit()
        B.append(row)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                matr_multiply[i][j] += A[i][k]*B[k][j]
    for i in matr_multiply:
        print(' '.join(map(str, i)))
else:
    print('Error')