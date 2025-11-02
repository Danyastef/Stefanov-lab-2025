import subprocess
import pytest

INTERPRETER = 'python'

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
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird'),
        ('120', 'Error'),
        ('-120', 'Error')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['100000000000', '56'], ['Error']),
        (['10', '-30'], ['Error'])
    ],
    'division': [
        (['3','5'],['0','0.6']),
        (['2','4'],['0','0.5']),
        (['7','5'],['1','1.4']),
        (['5','0'],['Error'])
    ],
    'loops': [
        (['3'], ['0','1','4']),
        (['25'], ['Error']),
        (['-3'], ['Error'])
    ],
    'print_function': [
        ('-3', 'Error'),
        ('5', '12345'),
        ('22', 'Error')
    ],
    'second_score': [
        (['5', '2 3 6 6 5'], ['5']),
        (['3', '3 3 1'], ['1']),
        (['1', '5'], ['Error']),
        (['3', '3 3 3'], ['Error'])
    ],
    'nested_list': [
        (['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '41', 'Harsh', '39'], ['Berry', 'Harry']),
        (['3', 'Charlie', '50', 'Bob', '40', 'Alice', '50'], ['Alice', 'Charlie']),
        (['2', 'Sam', '60', 'John', '60'], ['Error']),
        (['1', 'Alex', '55'], ['Error'])
    ],
    'lists': [
        (['6', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print', 'remove 6', 'print'], ['[6, 5, 10]', '[5, 10]']),
        (['7', 'append 4', 'append 2', 'append 8', 'sort', 'print', 'reverse', 'print'], ['[2, 4, 8]', '[8, 4, 2]']),
        (['3', 'remove 10', 'append 5', 'print'], ['Error']),
        (['2', 'pop', 'pop'], ['Error']),
        (['2', 'insert 10 3', 'print'], ['Error']),
        (['0'], ['Error']),
        (['1', 'remov 1'], ['Error'])
    ],
    'swap_case': [
        ('Www.MosPolytech.ru','wWW.mOSpOLYTECH.RU'),
        ('Pythonist 2','pYTHONIST 2'),
        (' ','Error')
    ],
    'split_and_join': [
        ('this is a string','this-is-a-string'),
        (' ','')
    ],
    'max_word': [
        ('example.txt','сосредоточенности'),
    ],
    'price_sum': [
        ('products.csv','6842.84 5891.06 6810.9'),
    ],
    'anagram': [
        (['Able','bela'],['YES']),
        (['cafe','facc'],['NO']),
        (['Сон','нос'],['Error'])
    ],
    'metro': [
        (['3', '1 5', '2 6', '3 8', '3'], ['3']),
        (['3', '1 5', '2 6', '4 8', '6'], ['2']),
        (['2', '10 20', '15 25', '5'], ['0']),
        (['0', '5'], ['Error']),
        (['2', '5 10', '15 20', '-3'], ['Error']),
        (['2', '10 5', '15 20', '12'], ['Error'])
    ],
    'minion_game': [
        ('BANANA','Стюарт 12'),
        ('BANaNA','Error'),
        (' ','Error')
    ],
    'is_leap': [
        ('1800','Error'),
        ('1900','False'),
        ('2000','True'),
        ('2016','True'),
        ('2100','False')
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], ['1']),
        (['4 3', '2 4 5 7', '4 6 9', '1 2 5'], ['-1']),
        (['2 2', '2 4 5', '4 6', '1 2'], ['Error']),
        (['4 3', '2 4 5 7', '4 6', '1 2 5'], ['Error']),
        (['4 3', '2 4 5 7', '4 6 9', '1 2'], ['Error']),
        (['0 3', '', '4 6 9', '1 2 5'], ['Error']),
        (['3 0', '1 2 4', '', ''], ['Error']),
        (['3 3', '0 3 1', '4 6 9', '1 2 5'], ['Error'])
    ],
    'pirate_ship': [
        (['50 3','Золото 20 40', 'Серебро 50 50', 'Алмазы 35 600'], ['Алмазы 35 600', 'Золото 15 30.0']),
        (['0 3','Золото 20 40', 'Серебро 50 50', 'Алмазы 35 600'], ['Error']),
        (['50 0'], ['Error']),
        (['50 3','Золото 0 40', 'Серебро 50 50', 'Алмазы 35 600'], ['Error']),
        (['50 3','Золото 20 40', 'Серебро 50 0', 'Алмазы 35 600'], ['Error'])
    ],
    'matrix_mult': [
        (['3', '1 2 1', '4 2 2', '0 1 7', '7 5 1', '2 1 2', '4 3 4'], ['15 10 9', '40 28 16', '30 22 30']),
        (['11'], ['Error']),
        (['3', '1 2', '4 2 2', '0 1 7', '7 5 1', '2 1 2', '4 3 4'], ['Error']),
        (['3', '1 2 1', '4 2 2', '0 1 7', '7 5 1 3', '2 1 2', '4 3 4'], ['Error'])
    ]
}

def test_hello_world():
    assert run_script('hello.py') == 'Hello, World!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['max_word'])
def test_max_word(input_data, expected):
    assert run_script('max_word.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['price_sum'])
def test_price_sum(input_data, expected):
    assert run_script('price_sum.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    assert run_script('pirate_ship.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    assert run_script('matrix_mult.py', input_data).split('\n') == expected