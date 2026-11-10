import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'burger|nav-links|mobile-menu', text, re.IGNORECASE)]
print(f"Found {len(matches)} matches in script.js")
for pos in matches[:3]:
    start = max(0, pos - 40)
    end = min(len(text), pos + 300)
    print(f"--- Snippet: ---\n{text[start:end]}\n")
