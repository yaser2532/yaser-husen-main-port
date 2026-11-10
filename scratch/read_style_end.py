with open("assets/css/style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(max(0, len(lines)-40), len(lines)):
    print(f"{i+1}: {lines[i].rstrip()}")
