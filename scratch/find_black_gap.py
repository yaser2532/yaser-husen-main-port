import asyncio
from playwright.async_api import async_playwright

async def check_widths():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        viewports = [
            {'width': 375, 'height': 812, 'name': 'Mobile (375)'},
            {'width': 414, 'height': 896, 'name': 'Mobile (414)'},
            {'width': 768, 'height': 1024, 'name': 'Tablet (768)'},
            {'width': 1024, 'height': 768, 'name': 'Tablet (1024)'},
            {'width': 1440, 'height': 900, 'name': 'Desktop (1440)'},
            {'width': 1920, 'height': 1080, 'name': 'Desktop (1920)'}
        ]

        for vp in viewports:
            page = await browser.new_page(viewport={'width': vp['width'], 'height': vp['height']})
            await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
            await asyncio.sleep(1.0)

            # Check for elements sticking out to the right
            overflowing = await page.evaluate('''(viewWidth) => {
                const results = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const r = el.getBoundingClientRect();
                    if (r.right > viewWidth + 1 && r.width > 0) {
                        // check if visible
                        const comp = window.getComputedStyle(el);
                        if (comp.display !== 'none' && comp.visibility !== 'hidden' && comp.opacity !== '0') {
                            results.push({
                                tag: el.tagName,
                                id: el.id,
                                cls: el.className,
                                right: r.right,
                                width: r.width,
                                diff: r.right - viewWidth
                            });
                        }
                    }
                }
                return {
                    docScrollWidth: document.documentElement.scrollWidth,
                    bodyScrollWidth: document.body.scrollWidth,
                    windowInnerWidth: window.innerWidth,
                    hasDocOverflow: document.documentElement.scrollWidth > viewWidth,
                    hasBodyOverflow: document.body.scrollWidth > viewWidth,
                    overflowingCount: results.length,
                    topOverflowing: results.sort((a,b) => b.diff - a.diff).slice(0, 10)
                };
            }''', vp['width'])

            print(f"=== {vp['name']} ===")
            print(f"docScrollWidth: {overflowing['docScrollWidth']}, bodyScrollWidth: {overflowing['bodyScrollWidth']}, viewWidth: {overflowing['windowInnerWidth']}")
            print(f"hasDocOverflow: {overflowing['hasDocOverflow']}, hasBodyOverflow: {overflowing['hasBodyOverflow']}")
            if overflowing['topOverflowing']:
                print(f"Overflowing elements ({overflowing['overflowingCount']} total):")
                for item in overflowing['topOverflowing']:
                    print(f"  [{item['tag']}#{item['id']}.{item['cls'][:30]}] right={item['right']}, width={item['width']}, excess={item['diff']}px")
            else:
                print("  No overflowing elements detected via bounding rect.")
            print()

            await page.close()

        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_widths())
