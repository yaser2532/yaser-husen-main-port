import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

icons = re.findall(r'<i class=["\']([^"\']+)["\']', content)
print('Total icons found:', len(icons))
for icon in sorted(set(icons)):
    print('  -', icon)
