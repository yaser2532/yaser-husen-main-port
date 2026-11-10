import re

html_path = 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize CRLF to LF
text = content.replace('\r\n', '\n').replace('\r', '\n')

# 1. Remove cyber-marquee-section
marquee_pattern = r'<!-- Gen Z Kinetic Cyber Marquee Ticker Strip -->\s*<div class="cyber-marquee-section".*?</div>\s*</div>\s*</div>'
match = re.search(marquee_pattern, text, re.DOTALL)
if match:
    text = text[:match.start()] + text[match.end():]
    print("Removed cyber-marquee-section successfully.")
else:
    # Try alternate match if comments differ
    alt_pattern = r'<div class="cyber-marquee-section".*?</div>\s*</div>\s*</div>'
    match2 = re.search(alt_pattern, text, re.DOTALL)
    if match2:
        text = text[:match2.start()] + text[match2.end():]
        print("Removed cyber-marquee-section (alt match).")
    else:
        print("Warning: cyber-marquee-section not found!")

# 2. Remove all cyber-telemetry-strip blocks
strip_pattern = r'<div class="cyber-telemetry-strip">.*?</div>'
strips_found = len(re.findall(strip_pattern, text, re.DOTALL))
text = re.sub(strip_pattern, '', text, flags=re.DOTALL)
print(f"Removed {strips_found} cyber-telemetry-strip blocks.")

# Clean up multiple consecutive empty lines
text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

with open(html_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("index.html successfully updated!")
