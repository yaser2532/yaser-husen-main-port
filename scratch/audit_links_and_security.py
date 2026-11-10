import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check all internal anchor hashes
anchors = re.findall(r'href=["\']#([^"\']+)["\']', html)
all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
print('Total internal # targets:', len(anchors))
missing = [a for a in anchors if a not in all_ids]
print('Missing targets:', missing)

# Check all target="_blank" anchors lacking rel="noopener noreferrer"
pattern = re.compile(r'<a\s+([^>]*?)>', re.IGNORECASE | re.DOTALL)
needs_rel = []
for match in pattern.finditer(html):
    attrs = match.group(1)
    if 'target="_blank"' in attrs or "target='_blank'" in attrs:
        if 'rel="noopener noreferrer"' not in attrs and "rel='noopener noreferrer'" not in attrs:
            needs_rel.append(match.group(0))

print('Anchors with target="_blank" needing rel="noopener noreferrer":', len(needs_rel))
for a in needs_rel:
    print(' -', a)
