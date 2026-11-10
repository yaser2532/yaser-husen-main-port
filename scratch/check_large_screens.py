import asyncio
from playwright.async_api import async_playwright

async def inspect_large_viewports():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Test 1920x1080
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        # Check section widths and margins
        sections_info = await page.evaluate('''() => {
            const sections = document.querySelectorAll('header, section, footer, main, .container');
            const data = [];
            for (const s of sections) {
                const r = s.getBoundingClientRect();
                const comp = window.getComputedStyle(s);
                data.push({
                    tag: s.tagName,
                    id: s.id,
                    cls: (s.className || '').slice(0, 30),
                    left: Math.round(r.left),
                    right: Math.round(r.right),
                    width: Math.round(r.width),
                    maxWidth: comp.maxWidth,
                    marginLeft: comp.marginLeft,
                    marginRight: comp.marginRight
                });
            }
            return data;
        }''')
        for s in sections_info:
            print(f"[{s['tag']}#{s['id']}.{s['cls']}]: left={s['left']}, right={s['right']}, width={s['width']}, maxWidth={s['maxWidth']}, margin={s['marginLeft']} / {s['marginRight']}")

        # Take full page screenshot at 1920x1080 to visually see the right side
        await page.screenshot(path='scratch/viewport_1920_visual.png', full_page=False)

        # Also test 1440
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await asyncio.sleep(0.5)
        await page.screenshot(path='scratch/viewport_1440_visual.png', full_page=False)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_large_viewports())
