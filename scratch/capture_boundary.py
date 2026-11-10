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

        # Scroll so the boundary between hero and profile-expertise is right in the center of the viewport
        # header#home bottom is at y=900 (height 900)
        # If we scroll to y = 450, then the bottom of header#home is at client Y = 450 (middle of screen!)
        await page.evaluate("window.scrollTo(0, 450)")
        await page.wait_for_timeout(400)
        
        # Save screenshot
        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/boundary_mid_scroll.png"
        await page.screenshot(path=ss_path)
        print(f"Captured boundary at scroll=450: {ss_path}")

        # Check what elements exist around y=450 on screen
        elements = await page.evaluate('''() => {
            const h = document.getElementById('home');
            const p = document.getElementById('profile-expertise');
            const seam = document.querySelector('.hero-transition-seam');
            return {
                homeRect: h.getBoundingClientRect(),
                profileRect: p.getBoundingClientRect(),
                seamRect: seam ? seam.getBoundingClientRect() : null,
                elementsAtPoint: [
                    document.elementFromPoint(720, 440) ? document.elementFromPoint(720, 440).outerHTML.substring(0, 100) : null,
                    document.elementFromPoint(720, 450) ? document.elementFromPoint(720, 450).outerHTML.substring(0, 100) : null,
                    document.elementFromPoint(720, 460) ? document.elementFromPoint(720, 460).outerHTML.substring(0, 100) : null
                ]
            };
        }''')
        print("Elements around boundary at client Y=450:", elements)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
