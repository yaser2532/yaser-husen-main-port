with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

for s in ['.hero-sticker-badge', '.hero-clock-pill', '.trait-tag', '.profile-card-glow', '.badge']:
    p = css.find(s)
    if p != -1:
        print(f"=== {s} ===")
        print(css[p:p+300])
