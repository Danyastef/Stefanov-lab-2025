def wrapper(f):
    def fun(l):
        result = []
        for phone_num in l:
            phone_num = phone_num.lstrip('+7').lstrip('8').lstrip('0')
            if not phone_num.isdigit():
                return ['Error']
            if len(phone_num) == 10:
                result.append(f"+7 ({phone_num[:3]}) {phone_num[3:6]}-{phone_num[6:8]}-{phone_num[8:]}")
            else:
                return ['Error']
        return f(result)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
