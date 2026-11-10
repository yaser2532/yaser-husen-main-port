import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(500)

        # Apply symmetric straddling seam style
        await page.evaluate('''() => {
            const seam = document.querySelector('.hero-transition-seam');
            seam.style.position = 'absolute';
            seam.style.bottom = '-10rem';
            seam.style.left = '0';
            seam.style.width = '100%';
            seam.style.height = '20rem';
            seam.style.zIndex = '5';
            seam.style.pointerEvents = 'none';
            seam.style.background = 'linear-gradient(to bottom, transparent 0%, rgba(5, 2, 10, 0.40) 25%, rgba(4, 2, 8, 0.75) 50%, rgba(5, 2, 10, 0.40) 75%, transparent 100%)';
            seam.style.backdropFilter = 'blur(20px)';
            seam.style.webkitBackdropFilter = 'blur(20px)';
            seam.style.maskImage = 'linear-gradient(to bottom, transparent 0%, black 25%, black 75%, transparent 100%)';
            seam.style.webkitMaskImage = 'linear-gradient(to bottom, transparent 0%, black 25%, black 75%, transparent 100%)';
            
            // Also ensure header overflow is visible and z-index is high enough so it renders above background but below content
            const header = document.getElementById('home');
            header.style.overflow = 'visible';
            header.style.zIndex = '3';
        }''')

        await page.evaluate("window.scrollTo(0, 450)")
        await page.wait_for_timeout(300)

        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/test_straddling_seam.png"
        await page.screenshot(path=ss_path)
        print("Captured test_straddling_seam.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
