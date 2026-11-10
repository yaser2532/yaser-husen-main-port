from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/")

    sections = ['profile-expertise', 'about-me', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact']
    for sid in sections:
        info = page.evaluate(f'''() => {{
            const sec = document.getElementById("{sid}");
            if (!sec) return [];
            const selectors = [
                'h1, h2, h3, h4, .section-title, .card-title, .section-tag',
                '.section-desc, p, .about-text p, .trait-tag, .stat-label, .badge',
                '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card',
                '.profile-card-wrapper, .hero-traits-list, .filter-btn, .cta-button, .message-btn, .dock-btn, .cyber-dock-bar'
            ].join(', ');
            const cardSel = '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .cyber-dock-bar';
            const childNodes = Array.from(sec.querySelectorAll(selectors)).filter(childEl => {{
                if (childEl.matches(cardSel)) return true;
                if (childEl.closest(cardSel)) return false;
                return true;
            }});
            const getRank = (element) => {{
                const tag = element.tagName.toLowerCase();
                if (['h1', 'h2'].includes(tag) || element.classList.contains('section-title')) {{
                    return 0;
                }}
                if (element.classList.contains('section-desc') || element.classList.contains('section-tag') || tag === 'p') {{
                    return 1;
                }}
                if (element.matches('.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper')) {{
                    return 2;
                }}
                return 3;
            }};
            const sorted = childNodes.sort((a, b) => getRank(a) - getRank(b));
            return sorted.map((n, idx) => ({{
                rank: getRank(n),
                idx: idx,
                tag: n.tagName,
                cls: n.className.slice(0, 30),
                text: (n.textContent || '').trim().slice(0, 30).replace(/\\s+/g, ' ')
            }}));
        }}''')
        print(f"=== Section {sid} ({len(info)} items) ===")
        for item in info:
            safe_text = item['text'].encode('ascii', errors='replace').decode('ascii')
            print(f"  [Rank {item['rank']}] #{item['idx']} {item['tag']}.{item['cls']} -> {safe_text}")
    browser.close()
