with open('assets/js/nano-chat.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(function\s+[a-zA-Z0-9_]+\s*\([^)]*\)|const\s+[a-zA-Z0-9_]+\s*=\s*(?:function|\([^)]*\)\s*=>))', text)
print("Functions in nano-chat.js:")
for m in matches[:25]:
    print(" ", m)

# Let's search for open, pop, modal, or createElement
for line in text.split('\n'):
    if any(k in line.lower() for k in ['openchat', 'togglechat', 'createelement', 'chat-window', 'chat-card', 'class="', 'classlist.add']):
        print(line.strip()[:100].encode('ascii', 'replace').decode('ascii'))
