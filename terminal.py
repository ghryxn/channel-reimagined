# main_terminal.py
# CHANNEL TERMINAL v13.0 (clean + integrated with improved interpreter)

import os
import time
from interpreter import run_script
from parser import CHLParser, list_directory

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def prompt(cwd):
    now = time.localtime()
    return f"chl @ {time.strftime('%H:%M:%S %m-%d-%Y', now)} at {cwd}> "

def run_direct_command(command):
    parser = CHLParser(command)
    commands = parser.parse()
    for cmd, args in commands:
        args = args.strip()
        if cmd in ["text", "math", "mkdir", "mkfile", "cd", "ls", "dir", "runapp"]:
            # handle commands using run_chl style, but inline for direct input
            # we use run_chl for full scripts, here we just run single-line commands
            run_script_inline(cmd, args)
        else:
            print(f"[Unknown command: {args}]")

def run_script_inline(cmd, args):
    # minimal inline version of run_chl for direct input commands
    import subprocess, platform
    import os

    cwd = os.getcwd()

    if cmd == "text":
        print(args)
    elif cmd == "math":
        try:
            op, nums = args.split(maxsplit=1)
            num1, num2 = map(float, [n.strip() for n in nums.split(",")])
        except Exception:
            print("[Error] Invalid math syntax")
            return
        op = op.lower()
        if op == "add":
            print(num1 + num2)
        elif op == "subtract":
            print(num1 - num2)
        elif op == "multiply":
            print(num1 * num2)
        elif op == "divide":
            if num2 == 0:
                print("[Error] Cannot divide by zero")
            else:
                print(num1 / num2)
        else:
            print(f"[Error] Unknown operation: {op}")
    elif cmd == "mkdir":
        new_folder = os.path.join(cwd, args)
        try:
            os.makedirs(new_folder, exist_ok=True)
            print(f"[Folder created: {new_folder}]")
        except Exception as e:
            print(f"[Error] {e}")
    elif cmd == "mkfile":
        new_file = os.path.join(cwd, args)
        try:
            with open(new_file, "w", encoding="utf-8") as f:
                f.write("")
            print(f"[File created: {new_file}]")
        except Exception as e:
            print(f"[Error] {e}")
    elif cmd == "cd":
        new_path = os.path.expanduser(args)
        if platform.system() == "Windows" and len(new_path) == 2 and new_path[1] == ":":
            try:
                os.chdir(f"{new_path}\\")
                print(f"[Changed to drive {new_path.upper()}]")
            except Exception as e:
                print(f"[Error] {e}")
            return
        new_path = os.path.abspath(os.path.join(cwd, new_path))
        if os.path.exists(new_path) and os.path.isdir(new_path):
            try:
                os.chdir(new_path)
                print(f"[Changed directory to {os.getcwd()}]")
            except Exception as e:
                print(f"[Error] {e}")
        else:
            print(f"[Error] Path not found: {new_path}")
    elif cmd in ["ls", "dir"]:
        list_directory(cwd)
    elif cmd == "runapp":
        try:
            if os.name == "nt":
                os.startfile(args)
            else:
                subprocess.Popen(args, shell=True)
            print(f"[Running external app: {args}]")
        except Exception as e:
            print(f"[Error] Could not open {args}: {e}")

def main():
    clear()
    print("╔════════════════════════════════╗")
    print("║ CHANNEL TERMINAL v13.0        ║")
    print("║ Type 'help' for commands      ║")
    print("╚════════════════════════════════╝")

    cwd = os.getcwd()

    while True:
        cmd = input(prompt(cwd)).strip()

        if cmd == "exit":
            print("\nSee you next time.")
            break
        elif cmd == "clear":
            clear()
        elif cmd == "help":
            print("""Commands:
 run [file.chl] - Run a .chl script
 text [message] - Print text directly
 math [op] a, b - Do a math operation
 cd [path]      - Change directory or drive
 mkdir [name]   - Create a new folder
 mkfile [name]  - Create a new empty file
 ls / dir       - List files and folders
 runapp [prog]  - Run an external program
 clear          - Clear the screen
 exit           - Close the terminal""")
        elif cmd.startswith("run "):
            filename = cmd[4:].strip()
            full_path = os.path.join(cwd, filename)
            run_script(full_path)
        elif cmd.startswith(("text ", "math ", "mkdir ", "mkfile ", "cd ", "runapp ")):
            run_direct_command(cmd)
        elif cmd in ["ls", "dir"]:
            list_directory(cwd)
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()

