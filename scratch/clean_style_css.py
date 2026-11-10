import re

style_path = 'assets/css/style.css'

with open(style_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Pattern to remove marquee and telemetry styles
pattern = r'/\* --- 5\. GEN Z CHAOTIC KINETIC MARQUEE TICKER & TELEMETRY ACCENTS ---\s*\*/.*?(?=/\* Gen Z Holographic Project Card Stickers|\Z)'
match = re.search(pattern, text, re.DOTALL)
if match:
    text = text[:match.start()] + text[match.end():]
    print("Removed marquee and telemetry CSS.")
else:
    print("Warning: CSS pattern not found!")

# Clean multiple blank lines
text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

with open(style_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("style.css cleaned.")
