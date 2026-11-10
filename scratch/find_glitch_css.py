import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'glitch|gradient.*bar|split', text, re.IGNORECASE)]
print(f"Found {len(matches)} glitch/gradient occurrences in style.css")
for pos in matches[:8]:
    print(f"--- Pos {pos} ---")
    print(text[max(0, pos-40):min(len(text), pos+200)].replace('\n', ' '))
