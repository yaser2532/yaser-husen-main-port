import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(600)

        # Let's inspect every element around the bottom of #home and top of #profile-expertise
        elements = await page.evaluate('''() => {
            const results = [];
            const all = document.querySelectorAll('*');
            const home = document.getElementById('home');
            const homeRect = home.getBoundingClientRect();
            const boundaryY = homeRect.bottom; // in page coords: scrollY + homeRect.bottom

            all.forEach(el => {
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                
                // Check if element has any black or dark background, border, shadow, or hr
                const hasBorder = cs.borderTopWidth !== '0px' || cs.borderBottomWidth !== '0px';
                const bg = cs.backgroundColor;
                const hasBoxShadow = cs.boxShadow && cs.boxShadow !== 'none';
                
                // If element touches or is within 50px of the boundary
                if (Math.abs(r.bottom - boundaryY) < 100 || Math.abs(r.top - boundaryY) < 100) {
                    results.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        top: r.top,
                        bottom: r.bottom,
                        height: r.height,
                        bg: cs.backgroundColor,
                        bgImg: cs.backgroundImage ? cs.backgroundImage.substring(0, 80) : '',
                        borderTop: cs.borderTop,
                        borderBottom: cs.borderBottom,
                        boxShadow: cs.boxShadow,
                        backdropFilter: cs.backdropFilter || cs.webkitBackdropFilter
                    });
                }
            });
            return results;
        }''')

        print(f"Found {len(elements)} elements near boundary:")
        for el in elements:
            print(f"<{el['tag']} id='{el['id']}' class='{el['className'][:30]}'> top={el['top']}, btm={el['bottom']}")
            if el['borderTop'] != '0px none rgb(255, 255, 255)' and 'none' not in el['borderTop']:
                print(f"   borderTop: {el['borderTop']}")
            if el['borderBottom'] != '0px none rgb(255, 255, 255)' and 'none' not in el['borderBottom']:
                print(f"   borderBottom: {el['borderBottom']}")
            if el['bgImg'] and 'none' not in el['bgImg']:
                print(f"   bgImg: {el['bgImg']}")
            if el['bg'] and el['bg'] != 'rgba(0, 0, 0, 0)':
                print(f"   bg: {el['bg']}")
            if el['backdropFilter'] and el['backdropFilter'] != 'none':
                print(f"   backdropFilter: {el['backdropFilter']}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
