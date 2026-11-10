import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_mq = False
depth = 0
for i, line in enumerate(lines):
    if '@media' in line:
        in_mq = True
        print(f"--- Line {i+1}: {line.strip()} ---")
        for j in range(i, min(len(lines), i + 45)):
            print(f"{j+1}: {lines[j]}", end="")
        print("\n" + "="*50 + "\n")
