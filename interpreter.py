# channel_interpreter.py
# CHANNEL SCRIPT INTERPRETER (v3.1)
import os
import time
import platform
import subprocess
from parser import CHLParser

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
                print(f"  - {f}")
        else:
            print("  (no files)")

        print(f"\nSubdirectories in {cwd}")
        if folders:
            for d in folders:
                print(f"  - {d}")
        else:
            print("  (no subdirectories)")
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
        time.sleep(0.15)

        if cmd == "text":
            # ✅ preserve capitalization
            print(args)

        elif cmd == "math":
            try:
                parts = args.split()
                operation = parts[0].lower()
                numbers = args.split(operation)[1].strip().split(",")
                num1 = float(numbers[0])
                num2 = float(numbers[1])
            except Exception:
                print("[Error] Invalid math syntax")
                continue

            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    print("[Error] Cannot divide by zero")
                    continue
                result = num1 / num2
            else:
                print(f"[Error] Unknown operation: {operation}")
                continue
            print(result)

        elif cmd == "mkdir":
            folder_name = args.strip()
            new_folder = os.path.join(cwd, folder_name)
            try:
                os.makedirs(new_folder, exist_ok=True)
                print(f"[Folder created: {new_folder}]")
            except Exception as e:
                print(f"[Error] {e}")

        elif cmd == "mkfile":
            file_name = args.strip()
            new_file = os.path.join(cwd, file_name)
            try:
                with open(new_file, "w", encoding="utf-8") as f:
                    f.write("")  # empty file
                print(f"[File created: {new_file}]")
            except Exception as e:
                print(f"[Error] {e}")

        elif cmd == "cd":
            new_path = args.strip()
            if platform.system() == "Windows" and len(new_path) == 2 and new_path[1] == ":":
                try:
                    os.chdir(f"{new_path}\\")
                    cwd = os.getcwd()
                    print(f"[Changed to drive {new_path.upper()}]")
                except Exception as e:
                    print(f"[Error] {e}")
                continue

            new_path = os.path.expanduser(new_path)
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
            list_directory(os.getcwd())

        elif cmd == "runapp":
            program = args.strip()
            try:
                if os.name == "nt":
                    os.startfile(program)
                else:
                    subprocess.Popen(program.split())
                print(f"[Running external app: {program}]")
            except Exception as e:
                print(f"[Error] Could not open {program}: {e}")

        elif cmd == "unknown":
            print(f"[Unknown command: {args}]")

