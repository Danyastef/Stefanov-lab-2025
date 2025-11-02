import time
from fact import func_time 

def process_list(arr):
    if 1 <= len(arr) <= 10**3:
        return [i**2 if i % 2 == 0 else i**3 for i in arr]
    else:
        return 'Error'

def process_list_gen(arr):
    if 1 <= len(arr) <= 10**3:
        for i in arr:
            if i % 2 == 0:
                yield i**2
            else:
                yield i**3
    else:
        yield 'Error'

if __name__ == '__main__':
    arr = [5, 7, 4, 8, 2, 11, 6, 23, 78, 1, 35, 18, 9]
    list_time = func_time(process_list, arr)
    list_gen_time = func_time(process_list_gen, arr)
    print(f'Скорость работы с использованием list comprehension: {list_time} секунд')
    print(f'Скорость работы без list comprehension: {list_gen_time} секунд')

# Скорость работы функции без list comprehension меньше при работе с небольшими массивами