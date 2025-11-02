import functools
import datetime

def function_logger(path):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f_start = datetime.datetime.now()
            return_val = f(*args, **kwargs)
            f_end = datetime.datetime.now()
            running_time = f_end - f_start
            with open(path, 'a') as log:
                log.write(f"{f.__name__}\n")
                log.write(f"{f_start}\n")
                if args:
                    log.write(f"{args}\n")
                elif kwargs:
                    log.write(f"{kwargs}\n")
                else:
                    log.write("-\n")
                log.write(f"{return_val if return_val is not None else '-'}\n")
                log.write(f"{f_end}\n")
                log.write(f"{running_time}\n\n")
            return return_val
        return wrapper
    return decorator

if __name__ == "__main__":
    @function_logger('test.log')
    def greeting_format(name):
        return f'Hello, {name}!'
    greeting_format('John')