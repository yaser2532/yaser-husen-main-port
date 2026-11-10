import asyncio
import time
from playwright.async_api import async_playwright

async def test_build_spectacle():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        # Emulate 4x CPU throttle
        client = await context.new_cdp_session(page)
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        
        events = []
        page.on('console', lambda msg: events.append(f"LOG: {msg.text}") if 'drone' in msg.text.lower() else None)
        
        print("Navigating to http://localhost:8080/ ...")
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        # Measure scroll frame times
        print("Starting scroll performance trace...")
        frame_metrics = await page.evaluate('''() => {
            return new Promise((resolve) => {
                const frameTimes = [];
                let lastT = performance.now();
                let count = 0;
                
                function sample(now) {
                    const dt = now - lastT;
                    lastT = now;
                    frameTimes.push(dt);
                    count++;
                    if (count < 80) {
                        requestAnimationFrame(sample);
                    } else {
                        frameTimes.sort((a, b) => a - b);
                        const p95 = frameTimes[Math.floor(frameTimes.length * 0.95)];
                        const maxFrame = Math.max(...frameTimes);
                        resolve({ p95, maxFrame, frameCount: frameTimes.length });
                    }
                }
                
                // Simulate smooth scroll
                window.scrollTo({ top: 800, behavior: 'smooth' });
                requestAnimationFrame(sample);
            });
        }''')
        
        print(f"Scroll Frame Metrics (4x throttle): p95 = {frame_metrics['p95']:.2f} ms, max = {frame_metrics['maxFrame']:.2f} ms")
        
        # Dwell in profile-expertise to trigger gate
        print("Dwelling in profile-expertise for gate dispatch...")
        await page.wait_for_timeout(600)
        
        # Check active missions
        missions = await page.evaluate('''() => {
            const ms = window.drones.getMissions();
            const els = window.drones.getElements();
            return {
                activeCount: ms.length,
                expertiseElements: els.filter(e => e.secId === 'profile-expertise').map(e => ({
                    id: e.id,
                    type: e.type,
                    state: e.state,
                    duration: e.pullDuration
                }))
            };
        }''')
        print(f"Active missions: {missions['activeCount']}")
        for el in missions['expertiseElements']:
            print(f"  {el['id']} ({el['type']}): state={el['state']}, minDur={el['duration']}ms")
            
        # Capture screenshot during pull
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/spectacle_expertise_pulling.png')
        
        # Wait for full sequence to finish
        await page.wait_for_timeout(3000)
        await page.screenshot(path='scratch/spectacle_expertise_finished.png')
        
        # Now scroll to about-me to test code card
        print("Scrolling to #about-me ...")
        await page.evaluate("document.querySelector('#about-me').scrollIntoView({ behavior: 'smooth' })")
        await page.wait_for_timeout(800)
        
        # Dwell in about-me
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/spectacle_about_code_pulling.png')
        
        await page.wait_for_timeout(3000)
        await page.screenshot(path='scratch/spectacle_about_code_finished.png')
        
        # Check code line reveals
        code_lines = await page.evaluate('''() => {
            const lines = Array.from(document.querySelectorAll('.drone-code-line'));
            return {
                totalLines: lines.length,
                revealedLines: lines.filter(l => l.classList.contains('revealed')).length
            };
        }''')
        print("Code Lines Result:", code_lines)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_build_spectacle())
