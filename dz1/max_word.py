import re
name = input().strip()
with open(name, encoding="utf8") as file:
    text = file.read()
    words = re.findall(r'\b\w+\b', text)
    max_len = max(map(len, words))
    for word in words:
        if len(word) == max_len:
            print(word)