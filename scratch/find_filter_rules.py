import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.filter-btn' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i + 20)):
            print(f"  {lines[j].strip()}")
            if '}' in lines[j]:
                break
        print("="*40)
