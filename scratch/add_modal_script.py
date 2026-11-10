with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'nano-chat.js' in l:
        if 'card-popup-modal.js' not in ''.join(lines[i:i+4]):
            lines.insert(i+1, '    <script defer src="assets/js/card-popup-modal.js"></script>\n')
            print(f"Inserted card-popup-modal.js after line {i+1}")
        break

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
