with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(modal|popup|lightbox|pop-up|dialog)', text, re.IGNORECASE)
print("Matches in script.js for modal/popup/lightbox:", len(matches))

for l in text.split('\n'):
    if any(k in l.lower() for k in ['cert-modal', 'project-modal', 'card-modal', 'lightbox']):
        print(l.strip()[:100].encode('ascii', 'replace').decode('ascii'))
