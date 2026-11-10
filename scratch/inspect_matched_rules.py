import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(0.5)

        # Inspect styles
        res = await page.evaluate('''() => {
            const btn = document.querySelector('.project-filters .filter-btn');
            btn.classList.add('force-hover'); // test rule matching
            const s = document.createElement('style');
            s.innerHTML = '.force-hover { outline: 1px solid red; }';
            document.head.appendChild(s);

            // Check matching rules for .filter-btn
            const matched = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText && (rule.selectorText.includes('filter-btn') || rule.selectorText.includes('submit'))) {
                            matched.push({ sel: rule.selectorText, css: rule.style.cssText });
                        }
                    }
                } catch(e) {}
            }
            return matched.slice(-15);
        }''')
        for r in res:
            print("RULE:", r['sel'])
            print("  ->", r['css'][:120])
            print('-'*40)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
