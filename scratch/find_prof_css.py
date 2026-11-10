import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
found = []
while True:
    pos = text.find('profile-expertise', idx)
    if pos == -1:
        break
    found.append(pos)
    idx = pos + len('profile-expertise')

print(f"Found {len(found)} occurrences of profile-expertise in style.css")
for p in found:
    print(text[p-50:p+150])
    print('---')
