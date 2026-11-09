from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8080/')
    time.sleep(0.5)

    # Scroll directly to certificates halfway
    page.evaluate('''() => {
        const el = document.getElementById('certificates');
        const r = el.getBoundingClientRect();
        const targetY = window.scrollY + r.top + (r.height * 0.45) - (window.innerHeight * 0.5);
        window.scrollTo({ top: Math.max(0, targetY), behavior: 'instant' });
    }''')
    page.evaluate("window.dispatchEvent(new Event('scroll'))")

    # Check at 1400ms
    time.sleep(1.4)
    info = page.evaluate('''() => {
        const sec = document.getElementById('certificates');
        const r = sec.getBoundingClientRect();
        const nodes = Array.from(sec.querySelectorAll('[data-assembled]'));
        const allNodes = window.SectionCoordinator ? window.SectionCoordinator.getNodesForSection('certificates') : [];
        return {
            state: sec.getAttribute('data-nb'),
            rectTop: r.top,
            rectBottom: r.bottom,
            assembledCount: nodes.length,
            nodesDetails: allNodes.map((n, i) => ({
                idx: i,
                tag: n.el.tagName,
                cls: n.el.className.slice(0, 25),
                state: n.state,
                assembled: n.el.getAttribute('data-assembled'),
                opacity: getComputedStyle(n.el).opacity
            }))
        };
    }''')
    print('State:', info['state'])
    print('Rect:', info['rectTop'], 'to', info['rectBottom'])
    print('Assembled count:', info['assembledCount'])
    for n in info['nodesDetails']:
        print(n)
    browser.close()
