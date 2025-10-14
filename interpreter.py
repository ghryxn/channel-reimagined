# channel_interpreter.py
# CHANNEL SCRIPT INTERPRETER (v4.0)

import os
from parser import run_chl

def list_directory(cwd):
    """Optional: can be used if you want to call ls/dir outside a script."""
    try:
        files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
        folders = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]

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
        print("")  # spacing
    except Exception as e:
        print(f"[Error] {e}")

def run_script(file_path):
    """Run a .chl script using the improved parser and interpreter."""
    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return
    print(f"[Running {file_path}]\n")
    run_chl(file_path)
    print("\n[Done]")

# optional test when running this file directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_script(sys.argv[1])
    else:
        print("Usage: python channel_interpreter.py script.chl")

