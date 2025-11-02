def show_employee(name, salary = 100000):
    if salary < 0:
        return 'Error'
    return f'{name}: {salary} ₽'