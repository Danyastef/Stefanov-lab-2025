s = input().strip()
if 0 < len(s) <= 10**6 and all('A' <= c <= 'Z' for c in s):
    kevin_score = 0
    stuart_score = 0
    for i in range(len(s)):
        if s[i] in 'AEIOUY':
            kevin_score += len(s) - i
        else:
            stuart_score += len(s) - i
    if kevin_score > stuart_score:
        print('Кевин', kevin_score)
    else:
        print('Стюарт', stuart_score)
else:
    print('Error')