import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<header id="home"' in line:
        for j in range(max(0, i-5), min(len(lines), i+80)):
            l = lines[j].rstrip('\r\n')
            if l:
                print(f"{j+1}: {l}")
        break
