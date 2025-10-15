# editor.py
import os

def run_editor(file_path):
    # create file if not exists
    if not os.path.exists(file_path):
        open(file_path, "w").close()

    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    if not lines:
        lines = [""]

    print(f"\n[Editing {file_path}]")
    print("Type 'help' for editor commands.\n")

    def show():
        print("\n--- File Preview ---")
        for i, line in enumerate(lines, 1):
            print(f"{i:03d}: {line}")
        print("--------------------\n")

    show()

    while True:
        cmd = input("(edit)> ").strip()

        if cmd == "help":
            print("""
Commands:
  show              - Show file content again
  edit [n] [text]   - Replace line n with new text
  add [text]        - Add a new line at the end
  insert [n] [text] - Insert a new line before line n
  delete [n]        - Delete line number n
  save              - Save changes to file
  exit              - Exit editor without saving
  clear             - Clear the screen
""")

        elif cmd == "show":
            show()

        elif cmd.startswith("edit "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("[Error] Usage: edit [line_number] [new text]")
                continue
            try:
                n = int(parts[1])
                if n < 1 or n > len(lines):
                    print("[Error] Invalid line number")
                    continue
                lines[n - 1] = parts[2]
                print(f"[Edited line {n}]")
            except ValueError:
                print("[Error] Invalid number")

        elif cmd.startswith("add "):
            text = cmd[4:]
            lines.append(text)
            print("[Added new line]")

        elif cmd.startswith("insert "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("[Error] Usage: insert [line_number] [text]")
                continue
            try:
                n = int(parts[1])
                if n < 1 or n > len(lines) + 1:
                    print("[Error] Invalid position")
                    continue
                lines.insert(n - 1, parts[2])
                print(f"[Inserted before line {n}]")
            except ValueError:
                print("[Error] Invalid number")

        elif cmd.startswith("delete "):
            try:
                n = int(cmd.split()[1])
                if n < 1 or n > len(lines):
                    print("[Error] Invalid line number")
                    continue
                del lines[n - 1]
                print(f"[Deleted line {n}]")
            except (ValueError, IndexError):
                print("[Error] Invalid number")

        elif cmd == "save":
            with open(file_path, "w") as f:
                f.write("\n".join(lines))
            print(f"[Saved changes to {file_path}]")

        elif cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            show()

        elif cmd == "exit":
            print("[Exited editor]")
            break

        else:
            print("[Unknown command — type 'help']")
