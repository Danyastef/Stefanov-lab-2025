import sys

def my_sum_argv(*args):
    return sum(args)

if __name__ == "__main__":
    numbers = map(float, sys.argv[1:])
    print(my_sum_argv(*numbers))