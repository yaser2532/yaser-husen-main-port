import asyncio
from playwright.async_api import async_playwright

async def inspect_mobile_elements():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 375, "height": 812})
        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await asyncio.sleep(1.0)
        await page.evaluate("window.drones && window.drones.revealAll && window.drones.revealAll()")
        await asyncio.sleep(0.5)

        # Inspect specific components on 375px:
        # 1. Hero layout and pills
        hero_data = await page.evaluate("""() => {
            const h = document.getElementById('home');
            const pills = Array.from(h.querySelectorAll('.utc-clock-badge, .status-badge, .hero-details-container, .hero-cta-group, .hero-title, .hero-subtitle'));
            return pills.map(el => {
                const r = el.getBoundingClientRect();
                return { tag: el.tagName, cls: el.className, w: Math.round(r.width), h: Math.round(r.height), left: Math.round(r.left), right: Math.round(r.right) };
            });
        }""")
        print("Hero elements:")
        for hd in hero_data:
            print(" ", hd)

        # 2. About section stats and code block
        about_data = await page.evaluate("""() => {
            const sec = document.getElementById('about-me');
            const stats = Array.from(sec.querySelectorAll('.stats-row, .stat-card, .code-block-visual, .about-content'));
            return stats.map(el => {
                const r = el.getBoundingClientRect();
                return { tag: el.tagName, cls: el.className, w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right) };
            });
        }""")
        print("\nAbout elements:")
        for ad in about_data:
            print(" ", ad)

        # 3. Projects filter buttons and cards
        projects_data = await page.evaluate("""() => {
            const sec = document.getElementById('projects');
            const btns = Array.from(sec.querySelectorAll('.filter-btn, .projects-grid, .project-card'));
            return btns.map(el => {
                const r = el.getBoundingClientRect();
                return { cls: el.className.slice(0, 30), w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right) };
            });
        }""")
        print("\nProjects elements:")
        for pd in projects_data[:8]:
            print(" ", pd)

        # 4. Creative Lab / Birthday card & canvases
        bday_data = await page.evaluate("""() => {
            const sec = document.getElementById('creative-lab');
            const items = Array.from(sec.querySelectorAll('.bday-card, .cake-visual, .gift-box-visual, .star-map-visual, canvas'));
            return items.map(el => {
                const r = el.getBoundingClientRect();
                return { tag: el.tagName, id: el.id, cls: el.className.slice(0, 30), w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right) };
            });
        }""")
        print("\nCreative Lab elements:")
        for bd in bday_data:
            print(" ", bd)

        # 5. Contact form elements
        contact_data = await page.evaluate("""() => {
            const sec = document.getElementById('contact');
            const items = Array.from(sec.querySelectorAll('.contact-container, .contact-info, .contact-form, input, textarea, button'));
            return items.map(el => {
                const r = el.getBoundingClientRect();
                return { tag: el.tagName, cls: el.className.slice(0, 30), w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right) };
            });
        }""")
        print("\nContact elements:")
        for cd in contact_data[:8]:
            print(" ", cd)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_mobile_elements())
