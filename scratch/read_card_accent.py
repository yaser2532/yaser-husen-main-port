import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Top Accent Glitch Gradient Bar')
if pos != -1:
    print(text[pos-40:pos+1500])
