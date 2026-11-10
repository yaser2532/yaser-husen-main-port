import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2200, 2350):
    line = lines[i].rstrip('\r\n')
    if line:
        print(f"{i+1}: {line}")
