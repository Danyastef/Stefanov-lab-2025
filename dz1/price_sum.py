name = input().strip()
adult_spending = 0
pensioner_spending = 0
child_spending = 0
with open(name, encoding="utf8") as file:
    file.readline()
    for line in file:
        spendings = line.split(',')
        adult_spending += float(spendings[1])
        pensioner_spending += float(spendings[2])
        child_spending += float(spendings[3])
print(f'{round(adult_spending, 2)} {round(pensioner_spending, 2)} {round(child_spending, 2)}')