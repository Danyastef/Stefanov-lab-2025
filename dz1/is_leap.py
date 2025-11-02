def is_leap(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        else:
            return False
    elif year % 4 == 0:
        return True
    else:
        return False
year = int(input())
if 1900 <= year <= 10**5:   
    print(is_leap(year))
else:
    print("Error")