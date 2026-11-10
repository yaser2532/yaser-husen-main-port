import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/drones.css', 'rb') as f:
    raw = f.read()

eol = '\r\r\n' if b'\r\r\n' in raw else ('\r\n' if b'\r\n' in raw else '\n')
text = raw.decode('utf-8', errors='replace')

# Look for @media print block
idx_print = text.find('@media print {')
if idx_print != -1:
    idx_next_media = text.find('@media (prefers-reduced-motion', idx_print)
    if idx_next_media != -1:
        clean_print = """@media print {
    #nb-canvas, .hero-transition-seam { display: none !important; }
    html.drones-active [data-drone-state] {
        opacity: 1 !important;
        transform: none !important;
        filter: none !important;
    }
}

""".replace('\n', eol)
        text = text[:idx_print] + clean_print + text[idx_next_media:]

with open('assets/css/drones.css', 'wb') as f:
    f.write(text.encode('utf-8'))

print("Fixed @media print in drones.css.")
