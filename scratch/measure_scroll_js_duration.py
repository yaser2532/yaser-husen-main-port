import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-frame-rate-limit', '--disable-gpu-vsync', '--no-sandbox']
        )
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(1500)
        
        # Profile JS execution during scroll
        js_stats = await page.evaluate('''async () => {
            const scrollDurations = [];
            let scrollCount = 0;
            
            // Monitor scroll handler time
            const origScroll = window.onscroll;
            
            let start = performance.now();
            for (let i = 0; i < 40; i++) {
                const t0 = performance.now();
                window.scrollBy({ top: 60, behavior: 'instant' });
                const t1 = performance.now();
                scrollDurations.push(t1 - t0);
                await new Promise(r => requestAnimationFrame(r));
            }
            
            const avgScrollSync = scrollDurations.reduce((a,b)=>a+b,0) / scrollDurations.length;
            const maxScrollSync = Math.max(...scrollDurations);
            return {
                iterations: scrollDurations.length,
                avgScrollMs: avgScrollSync.toFixed(3),
                maxScrollMs: maxScrollSync.toFixed(3),
                finalScrollY: window.scrollY
            };
        }''')
        print("JS Execution during Scroll:", js_stats)
        
        # Check computed styles of profile card
        profile_data = await page.evaluate('''() => {
            const w = document.querySelector('.profile-card-wrapper');
            const img = document.querySelector('.profile-details-img');
            const csW = window.getComputedStyle(w);
            const csImg = window.getComputedStyle(img);
            return {
                wRadius: csW.borderRadius,
                wPadding: csW.padding,
                wBg: csW.backgroundImage || csW.background,
                imgRadius: csImg.borderRadius,
                imgBorder: csImg.border
            };
        }''')
        print("Profile Element Data:", profile_data)
        
        await browser.close()

asyncio.run(main())
