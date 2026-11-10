import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('creative-lab')
if pos != -1:
    print(text[pos-50:pos+1200])
