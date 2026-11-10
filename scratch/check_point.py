import asyncio
from playwright.async_api import async_playwright

async def check_element_at_point():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await asyncio.sleep(2)
        
        card_el = page.locator('.project-card').first
        await card_el.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        box = await card_el.bounding_box()
        
        target_x = box['x'] + 50
        target_y = box['y'] + 50
        
        el_info = await page.evaluate('''(pt) => {
            const topEl = document.elementFromPoint(pt.x, pt.y);
            return {
                tagName: topEl ? topEl.tagName : null,
                className: topEl ? topEl.className : null,
                id: topEl ? topEl.id : null,
                closestCard: topEl ? (topEl.closest('.project-card') !== null) : false
            };
        }''', {'x': target_x, 'y': target_y})
        print("Element at point:", el_info)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_element_at_point())
