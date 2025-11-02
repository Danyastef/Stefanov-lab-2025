import subprocess
import pytest
import math
import os
from plane_angle import Point

INTERPRETER = 'python3'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'fact': [
        (5, 120),
        (0, 'Error'),
        (10, 3628800),
        (10 ** 6, 'Error'),
    ],
    'show_employee': [
        ('Иванов Иван Иванович', None, 'Иванов Иван Иванович: 100000 ₽'),
        ('Иванов Иван Иванович', 300000, 'Иванов Иван Иванович: 300000 ₽'),
        ('Иванов Иван Иванович', -300000, 'Error')
    ],
    'sum_and_sub': [
        (10, 5, (15, 5))
    ],
    'process_list': [
        ([1, 2, 3, 4, 5], [1, 4, 27, 16, 125]),
        ([], 'Error'),
        ([1] * 10 ** 4, 'Error')
    ],
    'my_sum': [
        ((1, 2, 3, 4), 10),
        ((5, 2, 7), 14),
        ((8, 8, 9, 9, 2), 36)
    ],
    'my_sum_argv': [
        ((1, 2, 3, 4), 10),
        ((5, 2, 7), 14)
    ],
    'files_sort': [
        ('D:\\TechProj\\server', {'.cpp': ['Database.cpp', 'des.cpp', 'functions.cpp', 'main.cpp', 'mytcpserver.cpp'], '.db': ['DATABASE.db'], '.h': ['Database.h', 'des.h', 'functions.h', 'mytcpserver.h', 'sha1.h'], '.pro': ['echoServer.pro'], '.user': ['echoServer.pro.user'], '.m4a': ['muz.m4a'], '.mp3': ['muz.mp3'], '.txt': ['txt_for_test.txt']})
    ],
    'file_search': [
        ('txt_for_test.txt', ['Vasilev', 'Artem', '231-3213', 'Mospolytech', 'web-dev']),
        ('txxxxt.txt', None)
    ],
    'email_validation': [
        ('lara@mospolytech.ru', True),
        ('laramospolytech.ru', False),
        ('lara1@mospolytechru', False),
        ('la#ra@mospolytech.ru', False),
        ('lara@mosпolytech.ru', False),
        ('lara@mospolytech.r0u', False),
        ('lara@mospolytech.ruuu', False),
        ('лara@mospolytech.ru', False),
        ('lara@mospolytech.ком', False)
    ],
    'fibonacci': [
        (5, [0, 1, 1, 2, 3]),
        (0, 'Error'),
        (16, 'Error')
    ],
    'average_scores': [
        ([(89, 90, 78, 93, 80), (90, 91, 85, 88, 86), (91, 92, 83, 89, 90.5)], (90.0, 91.0, 82.0, 90.0, 85.5)),
        ([(89, 90, 78, 93, 80), (90, 91, 150, 88, 86), (91, 92, 83, 89, 90.5)], 'Error'),
        ([], 'Error'),
        ([(89, 90, 78, 93, 80) * 101], 'Error')
    ],
    'plane_angle': [
        (Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(1, 1, 1), 90),
        (Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 1), Point(2, 2, 2), 180)
    ],
    'phone_number': [
        (['07895462130', '89875641230', '9195969878'], ['+7 (789) 546-21-30', '+7 (919) 596-98-78', '+7 (987) 564-12-30']),
        (['07895462', '89875641230', '9195969878'], ['Error']),
        (['07895462', '89875f41230', '91959+)9878'], ['Error']),
        (['07895462', '89875641230', '91959698+78'], ['Error'])
    ],
    'people_sort': [
    ([['Mike', 'Thomson', '20', 'M'], ['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F']], ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle']),
    ([['John', 'Doe', '-5', 'M'], ['Alice', 'Smith', '30', 'F']], ['Error']),
    ([['John', 'Doe', '25', 'M']] * 11, ['Error']),
    ([], ['Error']),
    ],
    'complex_numbers_add': [
        (2, 1, 5, 6, '7.00+7.00i')
    ],
    'complex_numbers_sub': [
        (2, 1, 5, 6, '-3.00-5.00i')
    ],
    'complex_numbers_mul': [
        (2, 1, 5, 6, '4.00+17.00i')
    ],
    'complex_numbers_truediv': [
        (2, 1, 5, 6, '0.26-0.11i')
    ],
    'complex_numbers_mod': [
        (2, 1, '2.24+0.00i')
    ],
    'circle_square_mk': [
        (1, 1000, 3.072),
        (1, 10000, 3.1536)
    ]
}

from fact import fact_it, fact_rec
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from files_sort import sort_file_names
from file_search import file_search
from email_validation import fun
from fibonacci import fibonacci
from average_scores import compute_average_scores
from phone_number import sort_phone
from plane_angle import plane_angle
from people_sort import name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from log_decorator import function_logger

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_it(input_data, expected):
    assert fact_it(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_rec(input_data, expected):
    assert fact_rec(input_data) == expected

@pytest.mark.parametrize("name, salary, expected", test_data['show_employee'])
def test_show_employee(name, salary, expected):
    if salary is None:
        assert show_employee(name) == expected
    else:
        assert show_employee(name, salary) == expected

@pytest.mark.parametrize("a, b, expected", test_data['sum_and_sub'])
def test_sum_and_sub(a, b, expected):
    assert sum_and_sub(a, b) == expected

@pytest.mark.parametrize("input_data, expected", test_data['process_list'])
def test_process_list(input_data, expected):
    assert process_list(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['process_list'])
def test_process_list_gen(input_data, expected):
    assert process_list_gen(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['my_sum'])
def test_my_sum(input_data, expected):
    assert my_sum(*input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['my_sum_argv'])
def test_my_sum_argv(input_data, expected):
    assert my_sum_argv(*input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['files_sort'])
def test_sort_file_names(input_data, expected):
    assert sort_file_names(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['file_search'])
def test_file_search(input_data, expected):
    assert file_search(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['email_validation'])
def test_fun(input_data, expected):
    assert fun(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['fibonacci'])
def test_fibonacci(input_data, expected):
    assert fibonacci(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['average_scores'])
def test_compute_average_scores(input_data, expected):
    assert compute_average_scores(input_data) == expected

@pytest.mark.parametrize("a, b, c, d, expected", test_data['plane_angle'])
def test_plane_angle(a, b, c, d, expected):
    assert plane_angle(a, b, c, d) == expected

@pytest.mark.parametrize("input_data, expected", test_data['phone_number'])
def test_sort_phone(input_data, expected):
    assert sort_phone(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['people_sort'])
def test_name_format(input_data, expected):
    assert name_format(input_data) == expected

@pytest.mark.parametrize("a, b, c, d, expected", test_data['complex_numbers_add'])
def test_add(a, b, c, d, expected):
    assert str(Complex(a, b) + Complex(c, d)) == expected

@pytest.mark.parametrize("a, b, c, d, expected", test_data['complex_numbers_sub'])
def test_sub(a, b, c, d, expected):
    assert str(Complex(a, b) - Complex(c, d)) == expected

@pytest.mark.parametrize("a, b, c, d, expected", test_data['complex_numbers_mul'])
def test_mul(a, b, c, d, expected):
    assert str(Complex(a, b) * Complex(c, d)) == expected

@pytest.mark.parametrize("a, b, c, d, expected", test_data['complex_numbers_truediv'])
def test_truediv(a, b, c, d, expected):
    assert str(Complex(a, b) / Complex(c, d)) == expected

@pytest.mark.parametrize("a, b, expected", test_data['complex_numbers_mod'])
def test_mod(a, b, expected):
    assert str(Complex(a, b).mod()) == expected

@pytest.mark.parametrize("r, n, expected", test_data['circle_square_mk'])
def test_circle_square_mk(r, n, expected):
    expected_formul = math.pi * r ** 2
    assert abs(circle_square_mk(r, n) - expected_formul) / expected_formul < expected

def test_log_decorator():
    log_path = "test.log"
    if os.path.exists(log_path):
        os.remove(log_path)
    @function_logger(log_path)
    def sum(x, y):
        return x + y
    result = sum(2, 3)
    assert result == 5
    with open(log_path, "r") as log_file:
        log_content = log_file.read()
        assert "sum" in log_content
        assert "2, 3" in log_content
        assert "5" in log_content