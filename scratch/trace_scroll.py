from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8080/')
    time.sleep(0.5)

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
        print(f"\n--- Scrolling to {sid} ---")
        page.evaluate(f'''() => {{
            const el = document.getElementById("{sid}");
            const r = el.getBoundingClientRect();
            const targetY = window.scrollY + r.top + (r.height * 0.45) - (window.innerHeight * 0.5);
            window.scrollTo({{ top: Math.max(0, targetY), behavior: 'instant' }});
        }}''')
        page.evaluate("window.dispatchEvent(new Event('scroll'))")
        time.sleep(1.4)

        info = page.evaluate(f'''() => {{
            const sec = document.getElementById("{sid}");
            const r = sec.getBoundingClientRect();
            const assembled = sec.querySelectorAll('[data-assembled="true"]').length;
            const pullingSec = window.currentPullingItem ? window.currentPullingItem.id : (window.currPullItem ? window.currPullItem.id : 'none');
            return {{
                state: sec.getAttribute('data-nb'),
                top: r.top,
                bottom: r.bottom,
                assembled: assembled
            }};
        }}''')
        print(f"Section {sid}: state={info['state']}, top={info['top']}, bottom={info['bottom']}, assembled={info['assembled']}")

    browser.close()
