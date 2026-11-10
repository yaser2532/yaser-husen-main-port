import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-frame-rate-limit', '--disable-gpu-vsync', '--no-sandbox']
        )
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto("http://localhost:8080/")
        await page.wait_for_timeout(2000)
        
        # 1. Profile Verification
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
        print("1. Profile Data:", profile_data)
        assert profile_data['wRadius'] == '50%', f"Expected 50%, got {profile_data['wRadius']}"
        assert profile_data['imgRadius'] == '50%', f"Expected 50%, got {profile_data['imgRadius']}"
        assert 'linear-gradient' in profile_data['wBg'], "Expected linear-gradient in profile background"
        
        # 2. Scroll Responsiveness Test across entire page
        scroll_bench = await page.evaluate('''async () => {
            const frameDeltas = [];
            let last = performance.now();
            let active = true;
            
            function onFrame(now) {
                frameDeltas.push(now - last);
                last = now;
                if (active) requestAnimationFrame(onFrame);
            }
            requestAnimationFrame(onFrame);
            
            // Scroll down gradually
            for (let i = 0; i < 30; i++) {
                window.scrollBy(0, 150);
                await new Promise(r => setTimeout(r, 20));
            }
            // Scroll back up gradually
            for (let i = 0; i < 30; i++) {
                window.scrollBy(0, -150);
                await new Promise(r => setTimeout(r, 20));
            }
            active = false;
            await new Promise(r => setTimeout(r, 50));
            
            const measured = frameDeltas.slice(3);
            const avg = measured.reduce((a,b)=>a+b,0) / measured.length;
            const max = Math.max(...measured);
            return {
                totalFrames: measured.length,
                avgDelta: avg.toFixed(2),
                maxDelta: max.toFixed(2),
                finalY: window.scrollY
            };
        }''')
        print("2. Scroll Benchmark:", scroll_bench)
        
        # 3. Check for any console errors
        print("3. Console errors encountered:", len(console_errors))
        if console_errors:
            print("Errors:", console_errors)
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"
        
        print("\nALL VERIFICATIONS PASSED 100%!")
        await browser.close()

asyncio.run(main())
