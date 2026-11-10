import subprocess

# Check git show fa22bb3:index.html
res = subprocess.run(['git', 'show', 'fa22bb3:index.html'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
html = res.stdout

for line in html.splitlines():
    if 'code-block' in line or 'about-visual' in line or 'skills.matrix' in line:
        print(line)

# Let's inspect the lines around about-visual in fa22bb3
lines = html.splitlines()
for i, l in enumerate(lines):
    if 'about-visual' in l or 'code-block' in l:
        print(f"--- Line {i} ---")
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(f"{j}: {lines[j]}")
        break
