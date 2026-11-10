import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/hover-system.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of hover-system.js:", len(text.splitlines()))
print(text)
