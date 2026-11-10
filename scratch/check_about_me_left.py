import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(0.5)

        info = await page.evaluate('''() => {
            const el = document.querySelector("#about-me");
            const comp = window.getComputedStyle(el);
            const parentComp = window.getComputedStyle(el.parentElement);
            const bodyComp = window.getComputedStyle(document.body);
            const htmlComp = window.getComputedStyle(document.documentElement);
            return {
                aboutMe: {
                    rect: el.getBoundingClientRect(),
                    margin: `${comp.marginTop} ${comp.marginRight} ${comp.marginBottom} ${comp.marginLeft}`,
                    padding: `${comp.paddingTop} ${comp.paddingRight} ${comp.paddingBottom} ${comp.paddingLeft}`,
                    width: comp.width
                },
                parent: {
                    tag: el.parentElement.tagName,
                    cls: el.parentElement.className,
                    rect: el.parentElement.getBoundingClientRect(),
                    padding: `${parentComp.paddingTop} ${parentComp.paddingRight} ${parentComp.paddingBottom} ${parentComp.paddingLeft}`,
                    margin: `${parentComp.marginTop} ${parentComp.marginRight} ${parentComp.marginBottom} ${parentComp.marginLeft}`
                },
                body: {
                    rect: document.body.getBoundingClientRect(),
                    padding: `${bodyComp.paddingTop} ${bodyComp.paddingRight} ${bodyComp.paddingBottom} ${bodyComp.paddingLeft}`,
                    margin: `${bodyComp.marginTop} ${bodyComp.marginRight} ${bodyComp.marginBottom} ${bodyComp.marginLeft}`,
                    clientWidth: document.body.clientWidth,
                    scrollWidth: document.body.scrollWidth
                },
                html: {
                    clientWidth: document.documentElement.clientWidth,
                    scrollWidth: document.documentElement.scrollWidth,
                    padding: `${htmlComp.paddingTop} ${htmlComp.paddingRight} ${htmlComp.paddingBottom} ${htmlComp.paddingLeft}`,
                    margin: `${htmlComp.marginTop} ${htmlComp.marginRight} ${htmlComp.marginBottom} ${htmlComp.marginLeft}`
                }
            };
        }''')
        print(info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
