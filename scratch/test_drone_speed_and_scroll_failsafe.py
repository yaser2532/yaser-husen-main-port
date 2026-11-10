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
        await page.wait_for_timeout(1500)
        
        # 1. Verify durations in drones.js
        durations = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('[data-drone-state]'));
            // Check pull durations from first few pending items if stored or items
            return {
                totalMarked: els.length,
                builtAtStart: els.filter(e => e.getAttribute('data-drone-state') === 'built').length,
                pendingAtStart: els.filter(e => e.getAttribute('data-drone-state') === 'pending').length
            };
        }''')
        print("1. Elements at Start:", durations)
        
        # 2. Simulate user scrolling down smoothly through the sections
        for _ in range(15):
            await page.mouse.wheel(0, 300)
            await page.wait_for_timeout(100)
            
        mid_status = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('[data-drone-state]'));
            const states = {};
            els.forEach(e => {
                const s = e.getAttribute('data-drone-state');
                states[s] = (states[s] || 0) + 1;
            });
            return {
                scrollY: window.scrollY,
                states: states
            };
        }''')
        print("2. Status Mid-Scroll:", mid_status)
        
        # Scroll all the way down past projects, certificates, contact
        for _ in range(25):
            await page.mouse.wheel(0, 350)
            await page.wait_for_timeout(80)
            
        bottom_status = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('[data-drone-state]'));
            const states = {};
            els.forEach(e => {
                const s = e.getAttribute('data-drone-state');
                states[s] = (states[s] || 0) + 1;
            });
            return {
                scrollY: window.scrollY,
                states: states
            };
        }''')
        print("3. Status at Bottom (Past Sections):", bottom_status)
        
        # 4. Now test the FAIL-SAFE: Scroll back up to the top!
        # The user requested: "when he scrolls past it, then there is a fail-safe. If it comes back to the section, it should be already pulled out and rendered properly."
        for _ in range(30):
            await page.mouse.wheel(0, -400)
            await page.wait_for_timeout(50)
            
        await page.wait_for_timeout(500)
        
        scrolled_back_status = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('[data-drone-state]'));
            const unbuilt = els.filter(e => e.getAttribute('data-drone-state') !== 'built');
            const aboutSection = document.getElementById('about-me');
            const expertiseSection = document.getElementById('profile-expertise');
            const projectsSection = document.getElementById('projects');
            
            function checkSec(sec) {
                if (!sec) return 'not found';
                const items = Array.from(sec.querySelectorAll('[data-drone-state]'));
                return {
                    total: items.length,
                    built: items.filter(e => e.getAttribute('data-drone-state') === 'built').length,
                    pending: items.filter(e => e.getAttribute('data-drone-state') === 'pending').length
                };
            }
            
            return {
                finalScrollY: window.scrollY,
                totalElements: els.length,
                totalBuilt: els.filter(e => e.getAttribute('data-drone-state') === 'built').length,
                unbuiltCount: unbuilt.length,
                expertise: checkSec(expertiseSection),
                about: checkSec(aboutSection),
                projects: checkSec(projectsSection)
            };
        }''')
        print("4. Scrolled-Back-Up Fail-Safe Verification:", scrolled_back_status)
        
        # 5. Measure scroll performance (smoothness)
        scroll_perf = await page.evaluate('''async () => {
            let deltas = [];
            let last = performance.now();
            let running = true;
            function f(t) {
                deltas.push(t - last);
                last = t;
                if (running) requestAnimationFrame(f);
            }
            requestAnimationFrame(f);
            
            for (let i = 0; i < 20; i++) {
                window.scrollBy(0, 100);
                await new Promise(r => setTimeout(r, 20));
            }
            running = false;
            await new Promise(r => setTimeout(r, 60));
            
            const measured = deltas.slice(3);
            const avg = measured.reduce((a,b)=>a+b,0) / measured.length;
            const max = Math.max(...measured);
            return {
                frames: measured.length,
                avgDelta: avg.toFixed(2),
                maxDelta: max.toFixed(2)
            };
        }''')
        print("5. Scroll Performance (Wheel/Scroller):", scroll_perf)
        
        print("6. Console errors:", len(console_errors))
        if console_errors:
            print("Errors:", console_errors)
            
        # Take verification screenshot of sections when scrolled back up
        await page.screenshot(path="scratch/verified_scrolled_back_failsafe.png")
        print("Saved screenshot to scratch/verified_scrolled_back_failsafe.png")
        
        assert scrolled_back_status['unbuiltCount'] == 0, f"Expected 0 unbuilt, got {scrolled_back_status['unbuiltCount']}"
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"
        print("\nALL FAIL-SAFE & SCROLL CHECKS PASSED 100%!")
        
        await browser.close()

asyncio.run(main())
