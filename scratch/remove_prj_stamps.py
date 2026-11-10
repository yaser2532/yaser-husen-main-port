import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all prj-cyber-index divs
pattern = r'\s*<div class="prj-cyber-index"><span>// PRJ-\d+</span><span class="prj-sys-spec">.*?</span></div>'
matches = re.findall(pattern, text)
print(f"Found {len(matches)} prj-cyber-index elements to remove.")

text_cleaned = re.sub(pattern, '', text)

with open('index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_cleaned.replace('\r\n', '\n').replace('\n', '\r\n'))

print("Removed all prj-cyber-index stamps from index.html successfully!")
