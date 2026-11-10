with open("assets/css/style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(8500, min(len(lines), 8625)):
    if "filter-btn" in lines[i]:
        print(f"Line {i+1}: {lines[i].rstrip()}")
