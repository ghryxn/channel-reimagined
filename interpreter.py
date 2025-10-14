# channel_interpreter.py
import time
from parser import CHLParser

def run_chl(file_path):
    with open(file_path, "r") as f:
        source = f.read()

    parser = CHLParser(source)
    commands = parser.parse()

    for cmd, args in commands:
        time.sleep(0.3)  # <–– delay between each line

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
                print("[error] invalid math syntax")
                continue

            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    print("[error] cannot divide by zero")
                    continue
                result = num1 / num2
            else:
                print(f"[error] unknown operation: {operation}")
                continue

            print(result)

        elif cmd == "unknown":
            print(f"[unknown command: {args}]")

        # optional: little typing effect for realism
        time.sleep(0.1)
