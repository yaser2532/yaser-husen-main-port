import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def verify_v3():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        print("--- [V3] Testing Pipelining on in-band elements ---", flush=True)
        data = await page.evaluate("""async () => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
            
            const tStart = performance.now();
            let maxConcurrentCrews = 0;
            let inBandCompleted = false;
            let completionDuration = 0;
            const dispatchOrder = [];
            
            const bandTopY = window.innerHeight * 0.08;
            const bandBottomY = window.innerHeight * 0.88;
            
            // Elements that satisfy band (>= 80% visible)
            const inBandElements = window.drones.getElements().filter(e => {
                if (e.secId !== 'profile-expertise') return false;
                const r = e.el.getBoundingClientRect();
                const vTop = Math.max(r.top, bandTopY);
                const vBottom = Math.min(r.bottom, bandBottomY);
                const vH = Math.max(0, vBottom - vTop);
                return (vH >= r.height * 0.80);
            });
            
            for (let i = 0; i < 150; i++) {
                await new Promise(r => setTimeout(r, 20));
                const activeCrews = window.drones.getMetrics().activeCrewsCount;
                if (activeCrews > maxConcurrentCrews) {
                    maxConcurrentCrews = activeCrews;
                }
                
                const missions = window.drones.getMissions();
                missions.forEach(m => {
                    if (!dispatchOrder.includes(m.item.id)) {
                        dispatchOrder.push(m.item.id);
                    }
                });
                
                const builtCount = inBandElements.filter(e => e.state === 'built').length;
                if (builtCount === inBandElements.length && !inBandCompleted && inBandElements.length > 0) {
                    inBandCompleted = true;
                    completionDuration = (performance.now() - tStart) / 1000;
                    break;
                }
            }
            
            return {
                inBandCount: inBandElements.length,
                maxConcurrentCrews,
                inBandCompleted,
                completionDuration,
                dispatchOrder
            };
        }""")
        
        print("V3 Measured:", data, flush=True)
        v3_pass = (data['maxConcurrentCrews'] >= 2 and data['completionDuration'] <= 2.2 and data['inBandCompleted'])
        print(f"V3 Pass: {v3_pass} (Max Crews: {data['maxConcurrentCrews']}, Duration: {data['completionDuration']:.2f}s, Elements: {data['inBandCount']})", flush=True)
        await browser.close()

asyncio.run(verify_v3())
