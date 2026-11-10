import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'V6' in line:
        for j in range(max(0, i-2), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
