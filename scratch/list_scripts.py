import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for s in re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', text):
    print(s)
