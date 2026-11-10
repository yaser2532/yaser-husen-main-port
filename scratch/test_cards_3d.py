import asyncio
from playwright.async_api import async_playwright

async def inspect_cards():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Check React 3D Cards status
        status = await page.evaluate('''() => {
            return {
                hasReact: typeof React !== 'undefined',
                hasReactDOM: typeof ReactDOM !== 'undefined',
                reactVersion: typeof React !== 'undefined' ? React.version : null,
                react3DCard: typeof window.React3DCard !== 'undefined',
                controllersCount: window.React3DCard ? window.React3DCard.controllersCount() : 0,
                cardsWithReactClass: document.querySelectorAll('.react-3d-card').length,
                totalProjectCards: document.querySelectorAll('.project-card').length,
                totalExpertiseCards: document.querySelectorAll('.expertise-card').length,
                totalCertCards: document.querySelectorAll('.cert-card').length
            };
        }''')
        print("Status:", status)
        
        # Let's inspect a project card before hover
        card_el = page.locator('.project-card').first
        await card_el.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        
        box = await card_el.bounding_box()
        print("Card bounding box:", box)
        
        before_hover = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                transformStyle: cs.transformStyle,
                perspective: cs.perspective,
                transition: cs.transition,
                boxShadow: cs.boxShadow,
                inlineTransform: el.style.transform,
                droneState: el.getAttribute('data-drone-state')
            };
        }''', await card_el.element_handle())
        print("Before hover:", before_hover)
        
        # Now move mouse to top-left of the card (box['x'] + 30, box['y'] + 30)
        target_x = box['x'] + 30
        target_y = box['y'] + 30
        await page.mouse.move(target_x, target_y)
        await asyncio.sleep(0.4)
        
        during_hover_top_left = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                transformStyle: cs.transformStyle,
                perspective: cs.perspective,
                boxShadow: cs.boxShadow,
                inlineTransform: el.style.transform,
                inlineBoxShadow: el.style.boxShadow,
                classList: Array.from(el.classList)
            };
        }''', await card_el.element_handle())
        print("During hover (top-left):", during_hover_top_left)
        
        # Take screenshot of card hovered
        await card_el.screenshot(path='scratch/card_hover_test.png')
        print("Screenshot saved to scratch/card_hover_test.png")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_cards())
