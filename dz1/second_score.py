n = int(input())
A = list(map(int, input().split()))
if n > 1:
    max = float('-inf')
    second_max = float('-inf')
    for i in range(n):
        if A[i] > max:
            second_max = max
            max = A[i]
        elif A[i] > second_max and A[i] < max:
            second_max = A[i]
    if second_max == float('-inf'):
        print("Error")
    else:
        print(second_max)
else:
    print("Error")