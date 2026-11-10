import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['assets/js/hover-system.js', 'assets/css/style.css', 'assets/js/script.js']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"=== {fname} ===")
        matches = [m.start() for m in re.finditer(r'tilt|glitch|card.*hover|deform', text, re.IGNORECASE)]
        print(f"  Matches for tilt/glitch/card hover: {len(matches)}")
        for pos in matches[:4]:
            print(f"    {text[max(0, pos-30):min(len(text), pos+120)].replace('\n', ' ')}")
    except Exception as e:
        print(f"Error {fname}: {e}")
