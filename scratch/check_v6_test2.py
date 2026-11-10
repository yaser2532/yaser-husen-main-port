import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(65, 85):
    print(f"{i+1}: {lines[i].rstrip()}")
