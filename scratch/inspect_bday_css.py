import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

for word in ['cake-visual', 'gift-visual', 'gift-box', 'star-map', 'cakeCanvas', 'giftCanvas']:
    matches = [m.start() for m in re.finditer(re.escape(word), text)]
    print(f"'{word}': {len(matches)} matches")
    for pos in matches[:1]:
        start = max(0, pos - 40)
        end = min(len(text), pos + 200)
        print(f"  {text[start:end].replace('\n', ' ')}")
