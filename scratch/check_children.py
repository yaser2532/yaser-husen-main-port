import asyncio
from playwright.async_api import async_playwright

async def check_child_transforms():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        card = page.locator('.project-card').first
        await card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 150)")
        
        await page.wait_for_function("() => document.querySelector('.project-card')?.getAttribute('data-drone-state') === 'built'")
        
        box = await card.bounding_box()
        await page.mouse.move(box['x'] + 50, box['y'] + 50, steps=5)
        await asyncio.sleep(0.4)
        
        children_info = await page.evaluate('''(el) => {
            const img = el.querySelector('.project-img-container');
            const title = el.querySelector('.project-title');
            const badge = el.querySelector('.badge');
            const links = el.querySelector('.project-links');
            return {
                img: img ? window.getComputedStyle(img).transform : null,
                title: title ? window.getComputedStyle(title).transform : null,
                badge: badge ? window.getComputedStyle(badge).transform : null,
                links: links ? window.getComputedStyle(links).transform : null
            };
        }''', await card.element_handle())
        print("Children transforms:", children_info)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_child_transforms())
