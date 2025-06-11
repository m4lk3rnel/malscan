import sys
import yara
import os

def compile(rules):
    return yara.compile(filepath=rules)

def scan_file(compiled_rules, location):
    matches = compiled_rules.match(location)
    if matches:
        for match in matches:
            print("[DETECTED] rule: " + match.rule + ", file: " + location)

def scan_directory_recursively(compiled_rules, location):

    if location[len(location) - 1] != "/":
        location = location + "/"

    files = os.listdir(location)

    for file in files:
        file_path = location + file

        if os.path.isdir(file_path):
            scan_directory_recursively(compiled_rules, file_path)
            continue

        try:
            matches = compiled_rules.match(file_path)
        except:
            print("couldn't process file (skip): " + file_path)
            continue
            
        if matches:
            for match in matches:
                print("[DETECTED] rule: " + match.rule + ", file: " + file_path)

def scan_directory(compiled_rules, location):
        files = os.listdir(location)

        for file in files:
            file_path = location + file

            if os.path.isdir(file_path):
                print(file_path + " is a directory. Skipping.")
                continue

            matches = compiled_rules.match(file_path)
            if matches:
                for match in matches:
                    print("[DETECTED] rule: " + match.rule + ", file: " + file_path)

if len(sys.argv) != 3:
    print("")
    print("usage: python3 scanner.py <path_to_rules> <path_to_file/directory>")
    print("example: python3 scanner.py rules test/")

    rules = sys.argv[1]
    location = sys.argv[2]
    recursive = ""

    compiled_rules = compile(rules)

    if os.path.isdir(location):

        if location[len(location) - 1] != "/":

            location = location + "/"

        recursive = input("do you wish to scan recursively? (y/n) ")

        if recursive == "y":
            scan_directory_recursively(compiled_rules, location)
        elif recursive == "n":
            scan_directory(compiled_rules, location)
        else:
            print("invalid choice.")

    elif os.path.isfile(location):
        scan_file(compiled_rules, location)

    else:
        print("invalid location.")


