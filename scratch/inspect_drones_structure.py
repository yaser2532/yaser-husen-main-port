import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("File size:", len(text))
lines = text.splitlines()
print("Total lines:", len(lines))

for i, line in enumerate(lines):
    if line.strip().startswith('// ───') or line.strip().startswith('class ') or line.strip().startswith('function '):
        print(f"{i}: {line.strip()[:80]}")
