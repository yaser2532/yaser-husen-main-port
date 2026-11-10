with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(len(lines)-35, len(lines)):
    print(f"{j+1}: {lines[j]}", end="")
