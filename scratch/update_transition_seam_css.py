import sys

sys.stdout.reconfigure(encoding='utf-8')

CSS_PATH = 'assets/css/drones.css'

with open(CSS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

old_block_part = """.hero-transition-seam {
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 12rem;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(4, 2, 7, 0.25) 30%, 
        rgba(4, 2, 7, 0.65) 65%, 
        rgba(4, 2, 7, 0.95) 90%, 
        #040207 100%);
    display: block;
}"""

# Since content may have extra newlines or different spacing, let's use a regex
import re

pattern = re.compile(
    r'\.hero-transition-seam\s*\{[^}]*background:\s*linear-gradient\([^}]*\);?\s*display:\s*block;?\s*\}',
    re.DOTALL
)

new_block = """.hero-transition-seam {
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 14rem;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(4, 2, 7, 0.20) 25%, 
        rgba(4, 2, 7, 0.60) 60%, 
        rgba(4, 2, 7, 0.92) 88%, 
        #040207 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.4) 30%, black 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.4) 30%, black 100%);
    display: block;
}"""

match = pattern.search(content)
if not match:
    print("ERROR: could not find .hero-transition-seam rule")
    sys.exit(1)

content = content[:match.start()] + new_block + content[match.end():]

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated .hero-transition-seam CSS successfully!")
