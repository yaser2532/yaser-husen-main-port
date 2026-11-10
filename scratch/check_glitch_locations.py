import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('.hero-3d-char:hover,')
if pos1 != -1:
    print("--- hero-3d-char:hover ---")
    print(text[pos1:pos1+500])

pos2 = text.find('Top Accent Glitch Gradient Bar for Cards')
if pos2 != -1:
    print("\n--- Top Accent Glitch Gradient Bar ---")
    print(text[pos2:pos2+600])
