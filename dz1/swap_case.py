s = input().strip()
if 0 < len(s) <= 1000:
    result = ''.join(c.lower() if c.isupper() else c.upper() for c in s)
    print(result)
else:
    print("Error")