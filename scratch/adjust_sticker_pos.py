import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace multiple newlines with at most 2 newlines
text = re.sub(r'(\r?\n){3,}', '\n\n', text)
text = text.replace('\r\n', '\n')

# Update holo-sticker position
target = """.holo-sticker {
    position: absolute;
    top: 12px;
    right: 12px;"""

replacement = """.holo-sticker {
    position: absolute;
    top: -10px;
    right: 18px;"""

if target in text:
    text = text.replace(target, replacement)
    print("Updated holo-sticker position.")
else:
    print("Warning: target still not found.")

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(text.replace('\n', '\r\n'))

print("style.css normalized and saved.")
