import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 320, 'height': 568})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(500)

        overflowing = await page.evaluate('''() => {
            const docW = window.innerWidth;
            const els = Array.from(document.querySelectorAll('*'));
            const bad = [];
            els.forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.right > docW + 1) {
                    bad.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        right: r.right,
                        width: r.width,
                        overflowX: r.right - docW
                    });
                }
            });
            return bad.sort((a, b) => b.overflowX - a.overflowX).slice(0, 10);
        }''')
        print("Overflowing elements on 320px:")
        for o in overflowing:
            print(f"  {o['tag']}#{o['id']}.{o['className']}: width={o['width']:.1f}px, right={o['right']:.1f}px (overflow={o['overflowX']:.1f}px)")
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
