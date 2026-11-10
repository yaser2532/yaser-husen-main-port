import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8080/")
        await page.wait_for_timeout(2000)
        
        # Start recording frame times
        await page.evaluate('''() => {
            window.__frameDeltas = [];
            window.__lastTime = performance.now();
            window.__perfRunning = true;
            function loop(t) {
                const delta = t - window.__lastTime;
                window.__frameDeltas.push(delta);
                window.__lastTime = t;
                if (window.__perfRunning) requestAnimationFrame(loop);
            }
            requestAnimationFrame(loop);
        }''')
        
        # Simulate real user mouse wheel scrolling smoothly down the page
        for _ in range(30):
            await page.mouse.wheel(0, 80)
            await page.wait_for_timeout(35)
            
        stats = await page.evaluate('''() => {
            window.__perfRunning = false;
            const deltas = window.__frameDeltas.slice(2); // drop first startup frames
            const avg = deltas.reduce((a, b) => a + b, 0) / deltas.length;
            const max = Math.max(...deltas);
            const p95 = deltas.sort((a, b) => a - b)[Math.floor(deltas.length * 0.95)];
            const over33 = deltas.filter(d => d > 33.3).length;
            const scrollY = window.scrollY;
            return {
                frames: deltas.length,
                avgDelta: avg.toFixed(2),
                p95Delta: p95.toFixed(2),
                maxDelta: max.toFixed(2),
                framesOver33ms: over33,
                finalScrollY: scrollY
            };
        }''')
        
        print("Real Mouse Wheel Scroll Stats:", stats)
        
        # Take a screenshot of the circular profile image
        profile_el = await page.query_selector('.profile-card-wrapper')
        if profile_el:
            await profile_el.screenshot(path="scratch/verified_circular_profile.png")
            print("Captured circular profile screenshot at scratch/verified_circular_profile.png")
            
        await browser.close()

asyncio.run(main())
