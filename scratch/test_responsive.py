import asyncio
from playwright.async_api import async_playwright

async def test_responsive():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        viewports = [
            (320, 568),
            (375, 812),
            (768, 1024),
            (1024, 768),
            (1440, 900),
            (2560, 1440)
        ]
        
        results = []
        for w, h in viewports:
            page = await browser.new_page(viewport={'width': w, 'height': h})
            await page.goto('http://localhost:8080/', wait_until='networkidle')
            await page.wait_for_timeout(800)
            
            # Check horizontal scroll
            h_scroll = await page.evaluate('''() => {
                const scrollW = document.documentElement.scrollWidth;
                const clientW = document.documentElement.clientWidth;
                return {
                    scrollW,
                    clientW,
                    hasHorizontalScroll: scrollW > clientW
                };
            }''')
            
            # Check 44px minimum touch targets on mobile
            touch_targets = 0
            if w <= 768:
                touch_targets = await page.evaluate('''() => {
                    const interactive = Array.from(document.querySelectorAll('a, button, input'));
                    const tooSmall = interactive.filter(el => {
                        const r = el.getBoundingClientRect();
                        return (r.width > 0 && r.height > 0) && (r.width < 40 || r.height < 40);
                    });
                    return tooSmall.length;
                }''')
            
            results.append({
                'viewport': f'{w}x{h}',
                'scrollWidth': h_scroll['scrollW'],
                'clientWidth': h_scroll['clientW'],
                'horizontalOverflow': h_scroll['hasHorizontalScroll'],
                'smallTouchTargets': touch_targets
            })
            
            # Take responsive screenshot
            await page.screenshot(path=f'scratch/responsive_{w}.png')
            await page.close()
            
        import pprint
        pprint.pprint(results)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_responsive())
