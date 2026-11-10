from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/", wait_until="networkidle")
    
    # Scroll to profile-expertise
    page.evaluate("""() => {
        const el = document.getElementById('profile-expertise');
        if (el) el.scrollIntoView({ behavior: 'auto', block: 'center' });
    }""")
    page.wait_for_timeout(1000)

    debug = page.evaluate("""() => {
        const sec = document.getElementById('profile-expertise');
        const r = sec.getBoundingClientRect();
        const viewH = window.innerHeight;
        const visTop = Math.max(0, r.top);
        const visBottom = Math.min(viewH, r.bottom);
        const visHeight = Math.max(0, visBottom - visTop);
        const covers = (visHeight >= viewH * 0.42) || (r.top <= viewH * 0.45 && r.bottom >= viewH * 0.50);

        const els = window.drones.getElements();
        const profEls = els.filter(e => e.secId === 'profile-expertise');

        return {
            viewH,
            rTop: r.top,
            rBottom: r.bottom,
            visHeight,
            ratio: visHeight / viewH,
            covers,
            secInfoDwellMet: profEls[0] ? profEls[0].secInfo.dwellMet : null,
            profStates: profEls.map(e => ({
                id: e.id,
                type: e.type,
                state: e.state,
                top: e.el.getBoundingClientRect().top
            }))
        };
    }""")
    print("DEBUG:", debug)
    browser.close()
