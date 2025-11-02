import sys
import os

def sort_file_names(path):
    sorted_files = {}
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath):
            file_extension = os.path.splitext(file)[1]
            if file_extension not in sorted_files:
                sorted_files[file_extension] = []
            sorted_files[file_extension].append(file)
    sorted(sorted_files.keys())
    return sorted_files

if __name__ == "__main__":
    path = sys.argv[1]
    sorted_files = sort_file_names(path)
    for key in sorted_files:
        for file in sorted_files[key]:
            print(file)