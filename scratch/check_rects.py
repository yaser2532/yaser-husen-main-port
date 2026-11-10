from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://localhost:8080')
    page.wait_for_timeout(1000)
    data = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('.nb-section-wrap')).map(el => {
            const r = el.getBoundingClientRect();
            return {
                id: el.id,
                top: r.top + window.scrollY,
                bottom: r.bottom + window.scrollY,
                height: r.height,
                dataNb: el.getAttribute('data-nb')
            };
        });
    }""")
    for d in data:
        print(d)
    b.close()
