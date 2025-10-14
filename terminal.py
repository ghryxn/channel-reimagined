# main_terminal.py
# CHANNEL TERMINAL v12.0b (with ls/dir listing)
import os
import time
import subprocess
import platform
from interpreter import run_chl
from parser import CHLParser

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def prompt(cwd):
    now = time.localtime()
    formatted_time = time.strftime("%H:%M:%S", now)
    formatted_date = time.strftime("%m-%d-%Y", now)
    return f"chl @ {formatted_time} {formatted_date} at {cwd}> "

def run_direct_command(command):
    parser = CHLParser(command)
    commands = parser.parse()

    for cmd, args in commands:
        if cmd == "text":
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
        elif cmd == "unknown":
            print(f"[Unknown command: {args}]")

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

def main():
    clear()
    print("╔══════════════════════════════╗")
    print("║   CHANNEL TERMINAL  v12.0b   ║")
    print("║   Type 'help' for commands   ║")
    print("╚══════════════════════════════╝")

    cwd = os.getcwd()

    while True:
        cmd = input(prompt(cwd)).strip()

        if cmd == "exit":
            print("\nSee you next time.")
            break

        elif cmd == "clear":
            clear()

        elif cmd == "help":
            print("""
Commands:
  run [file.chl]       - Run a .chl script
  text [message]       - Print text directly
  math [op] a, b       - Do a math operation
  cd [path]            - Change directory or drive
  mkdir [name]         - Create a new folder
  mkfile [name]        - Create a new empty file
  ls / dir             - List files and folders cleanly
  runapp [program]     - Run an external program
  clear                - Clear the screen
  exit                 - Close the terminal
""")

        elif cmd.startswith("run "):
            filename = cmd[4:].strip()
            full_path = os.path.join(cwd, filename)
            if not os.path.exists(full_path):
                print(f"[Error] File not found: {filename}")
                continue
            print(f"[Running {full_path}]\n")
            run_chl(full_path)
            print("\n[Done]")

        elif cmd.startswith("text ") or cmd.startswith("math "):
            run_direct_command(cmd)

        elif cmd.startswith("cd "):
            new_path = cmd[3:].strip()
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

        elif cmd.startswith("mkdir "):
            folder_name = cmd[6:].strip()
            new_folder = os.path.join(cwd, folder_name)
            try:
                os.makedirs(new_folder, exist_ok=True)
                print(f"[Folder created: {new_folder}]")
            except Exception as e:
                print(f"[Error] {e}")

        elif cmd.startswith("mkfile "):
            file_name = cmd[7:].strip()
            new_file = os.path.join(cwd, file_name)
            try:
                with open(new_file, "w") as f:
                    f.write("")  # make empty file
                print(f"[File created: {new_file}]")
            except Exception as e:
                print(f"[Error] {e}")

        elif cmd.startswith("runapp "):
            program = cmd[7:].strip()
            try:
                if os.name == "nt":
                    os.startfile(program)
                else:
                    subprocess.Popen(program.split())
                print(f"[Running external app: {program}]")
            except Exception as e:
                print(f"[Error] Could not open {program}: {e}")

        elif cmd == "ls" or cmd == "dir":
            list_directory(cwd)

        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
