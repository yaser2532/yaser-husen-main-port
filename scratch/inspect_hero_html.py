import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find hero section or header
pos_hero = html.find('class="hero')
if pos_hero == -1:
    pos_hero = html.find('id="hero')
if pos_hero == -1:
    pos_hero = html.find('<header')

print("Hero position:", pos_hero)
print(html[pos_hero:pos_hero+2500])
