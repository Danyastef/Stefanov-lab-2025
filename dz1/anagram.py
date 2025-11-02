str1 = input().strip()
str2 = input().strip()
words1 = []
words2 = []
for word in str1:
    if 0 <= ord(word) <= 127:
        words1.append(word.lower())
    else:
        print('Error')
        exit()
for word in str2:
    if 0 <= ord(word) <= 127:
        words2.append(word.lower())
    else:
        print('Error')
        exit()
if sorted(words1) == sorted(words2):
    print('YES')
else:
    print('NO')