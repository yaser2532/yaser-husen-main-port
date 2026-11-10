import asyncio
from playwright.async_api import async_playwright

async def inspect_first_card():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await asyncio.sleep(2)
        
        info = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('.project-card'));
            return cards.map((c, idx) => {
                const rect = c.getBoundingClientRect();
                const cs = window.getComputedStyle(c);
                return {
                    idx,
                    title: c.querySelector('.project-title')?.innerText || '',
                    rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                    display: cs.display,
                    visibility: cs.visibility,
                    opacity: cs.opacity,
                    pointerEvents: cs.pointerEvents,
                    droneState: c.getAttribute('data-drone-state'),
                    parentClass: c.parentElement?.className
                };
            });
        }''')
        for item in info:
            print(item)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_first_card())
