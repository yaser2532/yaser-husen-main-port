import re

for filepath in ['assets/css/drones.css', 'assets/css/style.css', 'assets/js/drones.js']:
    with open(filepath, 'rb') as f:
        raw = f.read()
    # Normalize \r\n to \n
    text = raw.decode('utf-8', errors='ignore').replace('\r\n', '\n')
    # Collapse 3 or more newlines to at most 2 newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', text)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(cleaned)

print("Normalized newlines and line endings cleanly!")
