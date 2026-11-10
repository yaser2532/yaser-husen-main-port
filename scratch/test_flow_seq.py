from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8080/')
    sections = ['profile-expertise', 'about-me', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact']
    for sid in sections:
        info = page.evaluate(f'''() => {{
            const sec = document.getElementById("{sid}");
            if (!sec) return [];
            const selectors = [
                'h1, h2, h3, h4, .section-title, .card-title, .section-tag',
                '.section-desc, .section-intro, p, .about-text p, .trait-tag, .stat-label, .badge',
                '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper, .onboard-card',
                '.hero-traits-list, .filter-btn, .cta-button, .message-btn, .dock-btn, .cyber-dock-bar'
            ].join(', ');
            const cardSel = '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper, .cyber-dock-bar, .onboard-card';
            const childNodes = Array.from(sec.querySelectorAll(selectors)).filter(childEl => {{
                if (childEl.matches(cardSel)) return true;
                if (childEl.closest(cardSel)) return false;
                return true;
            }});
            const isTitle = (el) => {{
                const tag = el.tagName.toLowerCase();
                return ['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title');
            }};
            const sorted = childNodes.sort((a, b) => {{
                const aT = isTitle(a);
                const bT = isTitle(b);
                if (aT && !bT) return -1;
                if (!aT && bT) return 1;
                return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
            }});
            return sorted.map((n, i) => ({{
                idx: i,
                tag: n.tagName,
                cls: n.className.slice(0, 25),
                text: (n.textContent || '').trim().slice(0, 30).replace(/\\s+/g, ' ')
            }}));
        }}''')
        print(f"=== Section {sid} ({len(info)} items) ===")
        for item in info:
            safe = item['text'].encode('ascii', errors='replace').decode('ascii')
            print(f"  #{item['idx']} {item['tag']}.{item['cls']} -> {safe}")
    browser.close()
