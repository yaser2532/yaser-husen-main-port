import asyncio
from playwright.async_api import async_playwright

async def test_drone_and_3d():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        # Scroll to #projects
        print("Scrolling to #projects...")
        await page.evaluate("document.querySelector('#projects').scrollIntoView({ behavior: 'smooth' })")
        
        # Wait until at least one .project-card has data-drone-state="built"
        print("Waiting for drone assembly...")
        for i in range(30):
            state = await page.evaluate('''() => {
                const card = document.querySelector('.project-card');
                return card ? {
                    droneState: card.getAttribute('data-drone-state'),
                    pointerEvents: window.getComputedStyle(card).pointerEvents,
                    opacity: window.getComputedStyle(card).opacity
                } : null;
            }''')
            print(f"[{i*0.5:.1f}s] Card state:", state)
            if state and state['droneState'] == 'built':
                break
            await asyncio.sleep(0.5)
            
        card_el = page.locator('.project-card').first
        box = await card_el.bounding_box()
        print("Built card box:", box)
        
        # Hover at top-left: normX ~ -0.7, normY ~ -0.7
        hover_x = box['x'] + box['width'] * 0.15
        hover_y = box['y'] + box['height'] * 0.15
        print(f"Hovering at ({hover_x}, {hover_y})...")
        await page.mouse.move(hover_x, hover_y)
        await asyncio.sleep(0.5)
        
        hover_state = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                inlineBoxShadow: el.style.boxShadow,
                classList: Array.from(el.classList)
            };
        }''', await card_el.element_handle())
        print("Hover state (top-left):", hover_state)
        
        # Hover at bottom-right: normX ~ +0.7, normY ~ +0.7
        hover_br_x = box['x'] + box['width'] * 0.85
        hover_br_y = box['y'] + box['height'] * 0.85
        print(f"Hovering at ({hover_br_x}, {hover_br_y})...")
        await page.mouse.move(hover_br_x, hover_br_y)
        await asyncio.sleep(0.5)
        
        hover_br_state = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                inlineBoxShadow: el.style.boxShadow
            };
        }''', await card_el.element_handle())
        print("Hover state (bottom-right):", hover_br_state)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_drone_and_3d())
