import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def trace_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        await page.add_init_script("""
            window._traceLog = [];
            const origSetAttr = Element.prototype.setAttribute;
            Element.prototype.setAttribute = function(name, val) {
                if (name === 'data-drone-state') {
                    window._traceLog.push({
                        time: performance.now(),
                        id: this.id || this.className,
                        state: val,
                        stack: (new Error().stack || '')
                    });
                }
                return origSetAttr.apply(this, arguments);
            };
        """)
        
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        print("Now scrolling to profile-expertise...", flush=True)
        scroll_start = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
            return performance.now();
        }""")
        
        for t in range(0, 1000, 100):
            await page.wait_for_timeout(100)
            data = await page.evaluate("""() => {
                const missions = window.drones.getMissions();
                const els = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
                return {
                    missions: missions.length,
                    missionStates: missions.map(m => ({ item: m.item.id, arrived: m.arrivedCount, state: m.item.state })),
                    states: els.map(e => ({ id: e.id, state: e.state }))
                };
            }""")
            print(f"T={t+100}ms: missions={data['missions']}, active={data['missionStates']}, states={data['states'][:3]}", flush=True)
            
        await browser.close()

asyncio.run(trace_scroll())
