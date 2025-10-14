# chl_parser.py
# improved CHL parser for .chl scripts
import os
import platform
import subprocess

class CHLParser:
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

            # store command & arguments
            self.commands.append((cmd, args))
        return self.commands

def list_directory(cwd):
    files = []
    folders = []
    try:
        for item in os.listdir(cwd):
            full_path = os.path.join(cwd, item)
            if os.path.isdir(full_path):
                folders.append(item)
            else:
                files.append(item)

        print(f"\nFiles in {cwd}")
        if files:
            for f in files:
                print(f" - {f}")
        else:
            print(" (no files)")

        print(f"\nSubdirectories in {cwd}")
        if folders:
            for d in folders:
                print(f" - {d}")
        else:
            print(" (no subdirectories)")
        print("")  # spacing line
    except Exception as e:
        print(f"[Error] {e}")

def run_chl(file_path):
    cwd = os.getcwd()
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    parser = CHLParser(source)
    commands = parser.parse()

    for cmd, args in commands:
        args = args.strip()
        # tiny pause to mimic typing
        import time
        time.sleep(0.15)

        if cmd == "text":
            print(args)

        elif cmd == "math":
            try:
                op, nums = args.split(maxsplit=1)
                num1, num2 = map(float, [n.strip() for n in nums.split(",")])
            except Exception:
                print("[Error] Invalid math syntax")
                continue

            op = op.lower()
            if op == "add":
                result = num1 + num2
            elif op == "subtract":
                result = num1 - num2
            elif op == "multiply":
                result = num1 * num2
            elif op == "divide":
                if num2 == 0:
                    print("[Error] Cannot divide by zero")
                    continue
                result = num1 / num2
            else:
                print(f"[Error] Unknown operation: {op}")
                continue
            print(result)

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
