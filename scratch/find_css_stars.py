import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'.{0,60}(?:star|cosmic|sky).{0,60}', text, re.IGNORECASE):
    print(m.group(0).strip())
