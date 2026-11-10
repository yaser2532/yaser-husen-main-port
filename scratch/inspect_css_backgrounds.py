import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for css_file in ['assets/css/style.css', 'assets/css/drones.css']:
    with open(css_file, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"\n==================== {css_file} ====================")
    for selector in ['header#home', '#home', '#profile-expertise', '.hero-transition-seam', 'body', 'main', '.page-body-content', '#cosmic-bg', '#cosmic-canvas', '.section-padding']:
        pattern = re.compile(rf'(?:^|\n)\s*({re.escape(selector)}[^{{]*\{{[^}}]*\}})', re.DOTALL)
        for m in pattern.finditer(text):
            # Print non-empty rules
            rule = m.group(1).strip()
            # Collapse multiple newlines for readability
            rule_clean = '\n'.join([line.strip() for line in rule.splitlines() if line.strip()])
            print(f"--- Rule for {selector} ---")
            print(rule_clean[:400])
