import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'<a\s+([^>]*?)>', re.IGNORECASE | re.DOTALL)
for match in pattern.finditer(text):
    attrs = match.group(1)
    if 'http' in attrs:
        print(f"External Link: <a {attrs.strip()}>")
