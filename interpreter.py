# channel_interpreter.py
# CHANNEL SCRIPT INTERPRETER v5.0
# fully supports variables, print, text, math with variables, and all previous commands

import os
import platform
import subprocess
import time

# global variable store
VARIABLES = {}

class CHLParser:
    """Simple parser for .chl scripts"""
    def __init__(self, source):
        self.source = source
        self.commands = []

    def parse(self):
        lines = self.source.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            self.commands.append((cmd, args))
        return self.commands

def list_directory(cwd):
    """List files and folders in cwd"""
    try:
        files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
        folders = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, f))]
        print(f"\nFiles in {cwd}")
        print("\n".join(f" - {f}" for f in files) if files else " (no files)")
        print(f"\nSubdirectories in {cwd}")
        print("\n".join(f" - {d}" for d in folders) if folders else " (no subdirectories)")
        print("")
    except Exception as e:
        print(f"[Error] {e}")

def run_chl(file_path):
    """Run a .chl script"""
    cwd = os.getcwd()
    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    parser = CHLParser(source)
    commands = parser.parse()

    for cmd, args in commands:
        args = args.strip()
        time.sleep(0.1)

        if cmd == "text":
            print(args)

        elif cmd == "var":
            # var x = 5
            try:
                name, value = args.split("=", maxsplit=1)
                name = name.strip()
                value = value.strip()
                # convert to number if possible
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

                # replace variables with values if they exist
                num1 = VARIABLES.get(num1_str, num1_str)
                num2 = VARIABLES.get(num2_str, num2_str)
                # convert to float if still string
                num1 = float(num1) if isinstance(num1, str) else num1
                num2 = float(num2) if isinstance(num2, str) else num2
            except Exception:
                print("[Error] Invalid math syntax")
                continue

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
                    cwd = os.getcwd()
                    print(f"[Changed to drive {new_path.upper()}]")
                except Exception as e:
                    print(f"[Error] {e}")
                continue
            new_path = os.path.abspath(os.path.join(cwd, new_path))
            if os.path.exists(new_path) and os.path.isdir(new_path):
                try:
                    os.chdir(new_path)
                    cwd = os.getcwd()
                    print(f"[Changed directory to {cwd}]")
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

        else:
            print(f"[Unknown command: {args}]")

# optional test from command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_chl(sys.argv[1])
    else:
        print("Usage: python channel_interpreter.py script.chl")
