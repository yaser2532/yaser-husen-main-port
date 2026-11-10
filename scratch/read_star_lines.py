import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Deep Universe Starfield')
if pos != -1:
    print(text[pos-40:pos+800])
