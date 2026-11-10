with open("assets/js/pull-build.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines, start=1):
    opens = line.count("{")
    closes = line.count("}")
    depth += opens - closes
    if depth < 0:
        print(f"Depth went negative at line {i}: {line.strip()}")
        break
print(f"Final depth: {depth}")
