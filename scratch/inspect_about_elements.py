import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)

        # Scroll to about-me
        await page.evaluate("document.getElementById('about-me').scrollIntoView()")
        await page.wait_for_timeout(1000)

        sec_info = await page.evaluate('''() => {
            const els = window.drones.getElements();
            const aboutEls = els.filter(e => e.sectionId === 'about-me');
            return aboutEls.map(e => ({
                tag: e.el.tagName,
                class: e.el.className,
                type: e.type,
                state: e.state,
                order: e.order,
                text: e.el.innerText.slice(0, 30)
            }));
        }''')
        print(f"About-Me Elements ({len(sec_info)}):")
        for e in sec_info:
            print(f"  [{e['state']}] {e['type']} (order {e['order']}) - {e['class']} - {repr(e['text'])}")

        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
