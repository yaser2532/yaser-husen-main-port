import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def debug_gate():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
        }""")
        await page.wait_for_timeout(200)
        
        eval_result = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const secRect = sec.getBoundingClientRect();
            const viewH = window.innerHeight;
            const bandTopY = viewH * 0.08;
            const bandBottomY = viewH * 0.88;
            
            const els = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
            const elChecks = els.map(item => {
                const r = item.el.getBoundingClientRect();
                const visibleTop = Math.max(r.top, bandTopY);
                const visibleBottom = Math.min(r.bottom, bandBottomY);
                const visibleHeight = Math.max(0, visibleBottom - visibleTop);
                const satisfiesBand = (visibleHeight >= r.height * 0.80);
                return {
                    id: item.id,
                    top: r.top,
                    bottom: r.bottom,
                    height: r.height,
                    satisfiesBand,
                    state: item.state
                };
            });
            
            const availableDrones = window.drones.getDrones().filter(d => d.state === 'FOLLOW').length;
            
            return {
                secRect: { top: secRect.top, bottom: secRect.bottom },
                dwellMet: els[0]?.secInfo?.dwellMet,
                band: { top: bandTopY, bottom: bandBottomY },
                elChecks,
                availableDrones
            };
        }""")
        print("Gate Debug:", eval_result, flush=True)
        await browser.close()

asyncio.run(debug_gate())
