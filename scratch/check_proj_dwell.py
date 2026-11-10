import asyncio
from playwright.async_api import async_playwright

async def check_proj_dwell():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        # Scroll to #projects
        await page.evaluate("document.querySelector('#projects').scrollIntoView({ behavior: 'auto' })")
        await asyncio.sleep(1)
        
        info = await page.evaluate('''() => {
            const sec = document.querySelector('#projects');
            const r = sec.getBoundingClientRect();
            const viewH = window.innerHeight;
            const bandTopY = viewH * 0.08;
            const bandBottomY = viewH * 0.88;
            const inBand = (r.bottom >= bandTopY && r.top <= bandBottomY + 60);
            
            // Check cards inside
            const cards = Array.from(sec.querySelectorAll('.project-card')).map(c => {
                const cr = c.getBoundingClientRect();
                return {
                    top: cr.top,
                    bottom: cr.bottom,
                    height: cr.height,
                    state: c.getAttribute('data-drone-state')
                };
            });
            
            return {
                scrollY: window.scrollY,
                r: { top: r.top, bottom: r.bottom },
                bandTopY,
                bandBottomY,
                inBand,
                cards
            };
        }''')
        print(info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_proj_dwell())
