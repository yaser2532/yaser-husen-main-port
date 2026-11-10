with open('assets/js/nano-chat.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'openModal =' in l:
        for j in range(i, min(len(lines), i+60)):
            print(f"{j+1}: {lines[j].encode('ascii', 'replace').decode('ascii').strip()}")
        break
