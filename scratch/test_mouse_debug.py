from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8080/', wait_until='domcontentloaded')
    page.wait_for_timeout(500)

    # Check before mouse move
    b4 = page.evaluate('''() => {
        const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
        const swarmData = window.swarm ? window.swarm.getDotsData() : [];
        return {
            dot0Transform: dots[0].style.transform,
            dot0Rect: dots[0].getBoundingClientRect(),
            dot0Data: swarmData[0]
        };
    }''')
    print("Before mouse move:", b4)

    # Dispatch mousemove directly on document
    page.evaluate('''() => {
        document.dispatchEvent(new MouseEvent('mousemove', { clientX: 600, clientY: 400 }));
    }''')
    page.wait_for_timeout(500)

    after = page.evaluate('''() => {
        const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
        const swarmData = window.swarm ? window.swarm.getDotsData() : [];
        return {
            dot0Transform: dots[0].style.transform,
            dot0Rect: dots[0].getBoundingClientRect(),
            dot0Data: swarmData[0]
        };
    }''')
    print("After mouse move:", after)
    browser.close()
