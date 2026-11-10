import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def measure_v1():
    print("--- [V1] Measuring Official Latency Benchmarks ---", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        await page.wait_for_timeout(1000)
        
        data = await page.evaluate("""() => {
            const el = window.drones.getElements().find(e => e.secId === 'profile-expertise');
            const m = window.drones.getMissions().find(m => m.item.id === el.id) || { flightDuration: 400, hivePulseDuration: 80 };
            const dispatchLatency = el.dispatchTime - el.gateOpenedTime;
            const revealLatency = el.pullStartTime - el.gateOpenedTime;
            const visibleFlight = el.pullStartTime - (el.dispatchTime + 80);
            return {
                gateOpenedTime: el.gateOpenedTime,
                dispatchTime: el.dispatchTime,
                pullStartTime: el.pullStartTime,
                dispatchLatency,
                revealLatency,
                visibleFlight
            };
        }""")
        
        print(f"Gate Open to First Dispatch: {data['dispatchLatency']:.1f} ms (req <= 150 ms)", flush=True)
        print(f"Gate Open to First Reveal: {data['revealLatency']:.1f} ms (req <= 450 ms)", flush=True)
        print(f"Visible Ribbon Flight: {data['visibleFlight']:.1f} ms (req >= 300 ms)", flush=True)
        
        v1_pass = (data['dispatchLatency'] <= 150 and data['revealLatency'] <= 450 and data['visibleFlight'] >= 300)
        print(f"V1 Pass: {v1_pass}", flush=True)
        await browser.close()

asyncio.run(measure_v1())
