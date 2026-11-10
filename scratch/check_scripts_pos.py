with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(3940, min(len(lines), 3980)):
    print(f"{i+1}: {lines[i].rstrip()}")
