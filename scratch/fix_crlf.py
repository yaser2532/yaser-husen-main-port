import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n').replace('\r', '\n')
text = re.sub(r'\n\s*\n+', '\n', text)
text = re.sub(r'}\s*\n(?=[.#a-zA-Z@])', '}\n\n', text)
text = text.replace('top: 12px;\n    right: 12px;', 'top: -10px;\n    right: 18px;')

with open('assets/css/style.css', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("Cleaned up style.css formatting perfectly.")
