import sys
import yara
import os

def compile(rules):
    return yara.compile(filepath=rules)

def scan(rules, location):
    compiled_rules = compile(rules)

    if os.path.isfile(location):
        match = compiled_rules.match(location)
        if match:
            print("hello detected!");
    
    elif os.path.isdir(location):

        files = os.listdir(location)
        for file in files:
            file_path = location + file
            match = compiled_rules.match(file_path)
            if match:
                print("detected: " + file_path);


if len(sys.argv) != 3:
    print("usage: python3 scanner.py <path_to_rules> <path_to_file/directory>")
else:
    rules = sys.argv[1]
    location = sys.argv[2]
    scan(rules, location)

