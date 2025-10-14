# chl_parser.py
# basic parser for .chl scripts

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

            if cmd == "text":
                self.commands.append(("text", args))

            elif cmd == "math":
                self.commands.append(("math", args))

            else:
                self.commands.append(("unknown", line))

        return self.commands
