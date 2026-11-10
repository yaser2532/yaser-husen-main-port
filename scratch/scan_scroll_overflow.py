import asyncio
from playwright.async_api import async_playwright

async def scan_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Test on 1440, 1024, 768, 375
        for width in [1440, 1024, 768, 375]:
            page = await browser.new_page(viewport={'width': width, 'height': 900})
            await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
            await asyncio.sleep(1.0)

            total_h = await page.evaluate('document.body.scrollHeight')
            print(f"--- Width: {width}px (Total Height: {total_h}px) ---")

            step = 600
            for y in range(0, total_h, step):
                await page.evaluate(f'window.scrollTo(0, {y})')
                await asyncio.sleep(0.15)

                res = await page.evaluate('''(w) => {
                    const docW = document.documentElement.scrollWidth;
                    const bodyW = document.body.scrollWidth;
                    const overflowing = [];
                    const all = document.querySelectorAll('*');
                    for (const el of all) {
                        const r = el.getBoundingClientRect();
                        if (r.right > w + 2 && r.width > 0) {
                            const comp = window.getComputedStyle(el);
                            if (comp.display !== 'none' && comp.visibility !== 'hidden') {
                                overflowing.push({
                                    tag: el.tagName,
                                    cls: (el.className || '').toString().slice(0, 30),
                                    id: el.id,
                                    right: Math.round(r.right),
                                    w: Math.round(r.width),
                                    excess: Math.round(r.right - w)
                                });
                            }
                        }
                    }
                    return {
                        docW: docW,
                        bodyW: bodyW,
                        overflowing: overflowing
                    };
                }''', width)

                if res['docW'] > width or res['bodyW'] > width or len(res['overflowing']) > 0:
                    print(f"  At Y={y}: docW={res['docW']}, bodyW={res['bodyW']}, overflowCount={len(res['overflowing'])}")
                    for item in res['overflowing'][:5]:
                        print(f"    -> [{item['tag']}#{item['id']}.{item['cls']}] right={item['right']}, excess={item['excess']}px")

            await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(scan_scroll())
