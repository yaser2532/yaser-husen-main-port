import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css_norm = css.replace('\r\n', '\n')

# Remove .prj-cyber-index and .prj-sys-spec rules
css_norm = re.sub(r'/\* Monospace Cyber Telemetry Metadata on Project Cards \*/\s*\.prj-cyber-index\s*\{[^}]*\}\s*\.prj-sys-spec\s*\{[^}]*\}', '', css_norm)

with open('assets/css/style.css', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(css_norm.replace('\n', '\r\n'))

print("Cleaned up prj-cyber-index styles from style.css!")
