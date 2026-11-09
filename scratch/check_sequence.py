import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect sections in index.html
section_ids = [
    "profile-expertise",
    "about-me",
    "projects",
    "creative-lab",
    "certificates",
    "secret-desk",
    "contact"
]

for sid in section_ids:
    m = re.search(r'<section[^>]*id=["\']' + sid + r'["\'][\s\S]*?(?=</section>|<section|$)', html)
    if not m:
        m = re.search(r'<footer[^>]*id=["\']' + sid + r'["\'][\s\S]*?(?=</footer>|$)', html)
    if m:
        sec_html = m.group(0)
        # Find all h2, p, and cards in order
        tags = re.findall(r'<(h[1-4]|p|div|button|a)\b([^>]*)>', sec_html)
        print(f"=== {sid} ===")
        seq = []
        for tag, attrs in tags:
            if tag in ['h1', 'h2', 'h3', 'h4']:
                seq.append(f"<{tag}>")
            elif tag == 'p' and ('section-desc' in attrs or 'about-text' in attrs or len(seq) < 4):
                seq.append(f"<p>")
            elif 'class=' in attrs:
                for cls in ['expertise-card', 'project-card', 'cert-card', 'glass-card', 'stat-card', 'cyber-dock-bar']:
                    if cls in attrs:
                        seq.append(f"<div.{cls}>")
                        break
        # Deduplicate consecutive identical card markers if any
        clean_seq = []
        for item in seq:
            if not clean_seq or item != clean_seq[-1] or not item.startswith('<div'):
                clean_seq.append(item)
        for idx, item in enumerate(clean_seq[:10]):
            print(f"  {idx}: {item}")
