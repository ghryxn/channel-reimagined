# main_terminal.py
# CHANNEL TERMINAL v13.1
# fully integrated with channel_interpreter.py v5.1
# supports var, print, text, math, mkdir, mkfile, cd, ls/dir, runapp

import os
import time
from interpreter import run_chl, CHLParser, list_directory, VARIABLES
from code_editor import run_editor

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
        # use the interpreter for all commands
        if cmd in ["text", "var", "print", "math", "mkdir", "mkfile", "cd", "ls", "dir", "runapp"]:
            run_chl_inline(cmd, args)
        else:
            print(f"[Unknown command: {args}]")

def run_chl_inline(cmd, args):
    """Run a single-line command interactively (like run_chl, but inline)"""
    import platform, subprocess

    cwd = os.getcwd()

    if cmd == "text":
        print(args)

    elif cmd == "var":
        try:
            name, value = args.split("=", maxsplit=1)
            name = name.strip()
            value = value.strip()
            if value.replace(".", "", 1).isdigit():
                value = float(value) if "." in value else int(value)
            VARIABLES[name] = value
        except Exception:
            print(f"[Error] Invalid var syntax: {args}")

    elif cmd == "print":
        if args in VARIABLES:
            print(VARIABLES[args])
        else:
            print(f"[Error] Variable '{args}' not found")

    elif cmd == "math":
        try:
            op, nums = args.split(maxsplit=1)
            num1_str, num2_str = [n.strip() for n in nums.split(",")]

            def resolve(val):
                if val in VARIABLES:
                    return VARIABLES[val]
                try:
                    return float(val) if '.' in val else int(val)
                except:
                    raise ValueError(f"Invalid operand: {val}")

            num1 = resolve(num1_str)
            num2 = resolve(num2_str)

        except Exception as e:
            print(f"[Error] Invalid math syntax: {e}")
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
    print("║ CHANNEL TERMINAL v13.1        ║")
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
 text [message] - Print raw text
 var [name] = [value] - Declare variable
 print [name]  - Print variable value
 math [op] a, b - Math operation (variables or numbers)
 cd [path]      - Change directory or drive
 mkdir [name]   - Create folder
 mkfile [name]  - Create empty file
 ls / dir       - List files and folders
 runapp [prog]  - Run external program
 clear          - Clear the screen
 exit           - Close terminal""")
        elif cmd.startswith("run "):
            filename = cmd[4:].strip()
            full_path = os.path.join(cwd, filename)
            run_chl(full_path)
        elif cmd.startswith(("text ", "var ", "print ", "math ", "mkdir ", "mkfile ", "cd ", "runapp ")):
            run_direct_command(cmd)
        elif cmd.startswith("edit "):
            filename = cmd[5:].strip()
            full_path = os.path.join(cwd, filename)
            run_editor(full_path)
        elif cmd in ["ls", "dir"]:
            list_directory(cwd)
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
