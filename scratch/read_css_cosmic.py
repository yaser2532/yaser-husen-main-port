import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '#cosmic-bg-container' in l or 'TRANSPARENT STARRY SKY' in l:
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j]}", end="")
        print("\n" + "="*50 + "\n")
