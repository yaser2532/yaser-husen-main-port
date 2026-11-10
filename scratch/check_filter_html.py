import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('project-filters')
if pos != -1:
    print(text[pos-40:pos+800])
