from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
import os
def test_get_files_info():
    tests = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),  #error outside working directory
        ("calculator", "../"),          
    ]
    for working_directory, directory in tests:
        result = get_files_info(working_directory, directory)
        print(result)

def test_get_file_content():
    tests = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),  #error outside working directory
        ("calculator", "pkg/does_not_exist.py"), #error file does not exist
    ]
    for working_directory, file_path in tests:
        result = get_file_content(working_directory, file_path)
        print(result)
        
def test_write_file():
    tests = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),  #error outside working directory
    ]
    for working_directory, file_path, content in tests:
        result = write_file(working_directory, file_path, content)
        print(result)

def test_run_python_file():
    tests = [
        ("calculator", "main.py", []),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", []), 
        ("calculator", "../main.py", []),  #error outside working directory
        ("calculator", "nonexistent.py", []),  #error file does not exist
    ]
    for working_directory, file_path, args in tests:
        result = run_python_file(working_directory, file_path, args)
        print(result)

if __name__ == "__main__":
    test_get_files_info()
    
    
    