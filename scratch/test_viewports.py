import asyncio
from playwright.async_api import async_playwright

async def audit_viewports():
    viewports = [
        ('mobile_320', 320, 600),
        ('mobile_375', 375, 667),
        ('mobile_414', 414, 896),
        ('tablet_768', 768, 1024),
        ('tablet_1024', 1024, 768),
        ('desktop_1440', 1440, 900),
        ('desktop_1920', 1920, 1080)
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for name, width, height in viewports:
            page = await browser.new_page(viewport={'width': width, 'height': height})
            await page.goto('http://localhost:8080/', wait_until='networkidle')
            await asyncio.sleep(0.5)
            
            overflow_data = await page.evaluate('''() => {
                const scrollWidth = document.documentElement.scrollWidth;
                const windowWidth = window.innerWidth;
                const hasOverflow = scrollWidth > windowWidth;
                
                return {
                    scrollWidth,
                    windowWidth,
                    hasOverflow,
                    overflowPx: scrollWidth - windowWidth
                };
            }''')
            
            print(f"Viewport {name:12} ({width:4}x{height:4}): hasOverflow={overflow_data['hasOverflow']} (overflow={overflow_data['overflowPx']}px)")
            await page.close()
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(audit_viewports())
