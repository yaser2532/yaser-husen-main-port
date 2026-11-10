with open("assets/css/style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "filter-btn" in line:
        print(f"Line {i+1}: {line.strip()}")
        # print surrounding 5 lines
        start = max(0, i-2)
        end = min(len(lines), i+8)
        for j in range(start, end):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 40)
