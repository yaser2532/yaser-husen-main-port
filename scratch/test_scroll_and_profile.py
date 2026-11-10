import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8080/")
        await page.wait_for_timeout(1500)
        
        # Profile styling check
        profile_style = await page.evaluate('''() => {
            const el = document.querySelector('.profile-card-wrapper');
            const img = document.querySelector('.profile-details-img');
            if (!el || !img) return null;
            const csEl = window.getComputedStyle(el);
            const csImg = window.getComputedStyle(img);
            return {
                wrapperRadius: csEl.borderRadius,
                wrapperBorder: csEl.border,
                wrapperBg: csEl.background,
                wrapperBoxShadow: csEl.boxShadow,
                imgRadius: csImg.borderRadius
            };
        }''')
        print("Profile Styles Currently:", profile_style)
        
        # Measure scroll frame rate / jitter
        scroll_stats = await page.evaluate('''async () => {
            let frameTimes = [];
            let lastTime = performance.now();
            let running = true;
            
            function onFrame(t) {
                frameTimes.push(t - lastTime);
                lastTime = t;
                if (running) requestAnimationFrame(onFrame);
            }
            requestAnimationFrame(onFrame);
            
            // Perform programmatic scroll simulation simulating wheel scroll
            for (let i = 0; i < 20; i++) {
                window.scrollBy({ top: 180, behavior: 'instant' });
                await new Promise(r => setTimeout(r, 30));
            }
            running = false;
            await new Promise(r => setTimeout(r, 100));
            
            let dropped = frameTimes.filter(t => t > 25).length;
            let maxDelta = Math.max(...frameTimes);
            let avgDelta = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
            return { totalFrames: frameTimes.length, droppedFrames: dropped, maxDelta, avgDelta };
        }''')
        print("Scroll Stats Currently:", scroll_stats)
        
        await browser.close()

asyncio.run(main())
