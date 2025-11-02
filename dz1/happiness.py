n, m = map(int, input().split())
if 1 <= n <= 10**5 and 1 <= m <= 10**5:
    arr = list(map(int, input().split()))
    A = set(map(int, input().split()))
    B = set(map(int, input().split()))
    if len(arr) != n or len(A) != m or len(B) != m or any(num < 1 or num > 10**9 for num in arr) or any(num < 1 or num > 10**9 for num in A | B):
        print("Error")
    else:
        happiness = 0
        for num in arr:
            if num in A:
                happiness += 1
            elif num in B:
                happiness -= 1
        print(happiness)    
else:
    print('Error')