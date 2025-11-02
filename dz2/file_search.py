import sys
import os

def file_search(filename):
    result = []
    file_directory = os.path.abspath(os.path.dirname(__file__))
    for path, folder, file in os.walk(file_directory):
        if filename in file:
            file_path = os.path.join(path, filename)
            print(file_path)
            with open(file_path, 'r', encoding="utf-8") as file:
                for i, line in enumerate(file):
                    if i < 5:
                        result.append(line.strip())
                    else:
                        break
            return result

    parent_directory = file_directory
    while True:
        parent_directory = os.path.abspath(os.path.join(parent_directory, ".."))
        for path, folder, files in os.walk(parent_directory):
            if filename in files:
                file_path = os.path.join(path, filename)
                print(file_path)
                with open(file_path, 'r', encoding="utf-8") as file:
                    for i, line in enumerate(file):
                        if i < 5:
                            result.append(line.strip())
                        else:
                            break
                return result
        if parent_directory == os.path.abspath(os.path.join(parent_directory, "..")):
            break
    return None

if __name__ == "__main__":
    filename = sys.argv[1]
    file_lines = file_search(filename)
    if file_lines != None:
        for line in file_lines:
            print(line)
    else:
        print(f"Файл {filename} не найден")