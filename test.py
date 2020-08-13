import os, sys, subprocess, time
from subprocess import PIPE

def test_folder(work_dir: str):
    """
    test sample cases
    ----------
    input
    work_dir: path of project folder
    work_dir must
    1. include "in"(test input folder) and "out"(test output folder)
        and file names in these folders must be same
    2. be one of cases bellow
        a. include "main.py"
        b. be maid by "cargo new"
        c. include "main.cpp" and "a.out"
        d. include "main.rs" and "main"
    """
    os.chdir(work_dir)
    if os.path.exists("main.py"):
        command = "python main.py"
    elif os.path.exists(os.path.join("target", "debug", os.path.basename(os.getcwd()))):
        command = os.path.join("target", "debug", os.path.basename(os.getcwd()))
    elif os.path.exists("main.cpp"):
        command = "./a.out"
    elif os.path.exists("main.rs"):
        command = "./main"
    else:
        print("Program file doesn't exist in the profect directory")
        sys.exit(1)

    assert(set(os.listdir("in")) == set(os.listdir("out")))
    cases = sorted(os.listdir("in"))
    print(f"Test {len(cases)} cases\n")
    num_passed = sum([test_case(command, os.path.join("in", case), os.path.join("out", case)) for case in cases])
    print(f"Pass: {num_passed}\nFail: {len(cases)-num_passed}")

def test_case(command: str,input_file: str, output_file: str):
    print(os.path.basename(input_file), end=" ")

    start = time.time()
    with open(input_file, 'r') as f:
        proc = subprocess.run(command, shell=True, stdin=f, stdout=PIPE, stderr=PIPE,)
    end = time.time()
    out = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")

    with open(output_file, 'r') as f:
        ans = f.read()

    if out == ans and end-start < 2:
        print(f"AC Time:{int(1000*(end-start))}ms\n")
        return True
    elif out == ans and end-start >= 2:
        print(f"TLE Time:{int(1000*(end-start))}ms\n")
        return False
    elif err != "":
        print("Error")
        print(f"{err}")
        return False
    else:
        print("WA")
        print(f"Out:\n{out}Answer:\n{ans}")
        return False

if __name__ == "__main__":
    print("Path of project directory:", end=" ")
    work_dir = input()
    test_folder(work_dir)
