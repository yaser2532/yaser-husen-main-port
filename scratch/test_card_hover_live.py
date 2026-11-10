import asyncio
from playwright.async_api import async_playwright

async def test_card_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        # Scroll to center the project card in the band
        card = page.locator('.project-card').first
        await card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 150)")
        
        # Wait for built
        await page.wait_for_function("() => document.querySelector('.project-card')?.getAttribute('data-drone-state') === 'built'")
        print("Card is built!")
        
        box = await card.bounding_box()
        print("Card box:", box)
        
        # Let's move the mouse over the card gradually
        # Point 1: Top-Left (normX ~ -0.7, normY ~ -0.7)
        tl_x = box['x'] + box['width'] * 0.15
        tl_y = box['y'] + box['height'] * 0.15
        print(f"Moving to top-left ({tl_x}, {tl_y})...")
        await page.mouse.move(tl_x, tl_y, steps=5)
        await asyncio.sleep(0.4)
        
        tl_info = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                inlineBoxShadow: el.style.boxShadow,
                classList: Array.from(el.classList)
            };
        }''', await card.element_handle())
        print("Top-left hover info:", tl_info)
        
        # Point 2: Bottom-Right (normX ~ +0.7, normY ~ +0.7)
        br_x = box['x'] + box['width'] * 0.85
        br_y = box['y'] + box['height'] * 0.85
        print(f"Moving to bottom-right ({br_x}, {br_y})...")
        await page.mouse.move(br_x, br_y, steps=5)
        await asyncio.sleep(0.4)
        
        br_info = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                inlineBoxShadow: el.style.boxShadow,
                classList: Array.from(el.classList)
            };
        }''', await card.element_handle())
        print("Bottom-right hover info:", br_info)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_card_hover())
