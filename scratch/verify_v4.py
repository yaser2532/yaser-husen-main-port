import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def verify_v4():
    print("--- [V4] Testing Random Procedural Paths across 3 reloads ---", flush=True)
    waypoints_across_runs = []
    
    async with async_playwright() as p:
        for run_id in range(3):
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1440, 'height': 900})
            await page.goto('http://localhost:8080/')
            await page.wait_for_timeout(600)
            
            await page.evaluate("""() => {
                const sec = document.getElementById('profile-expertise');
                window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
            }""")
            
            wps = None
            for _ in range(30):
                await page.wait_for_timeout(40)
                wps = await page.evaluate("""() => {
                    const m = window.drones.getMissions()[0];
                    if (!m || !m.crew || !m.crew[0] || !m.crew[0].pathPoints.length) return null;
                    return m.crew[0].pathPoints.map(p => ({ x: Math.round(p.x), y: Math.round(p.y) }));
                }""")
                if wps:
                    break
            
            print(f"Run {run_id + 1} Waypoints sample: {wps[:3] if wps else 'None'}", flush=True)
            waypoints_across_runs.append(wps)
            await browser.close()
            
    diff_1_2 = (waypoints_across_runs[0] != waypoints_across_runs[1])
    diff_2_3 = (waypoints_across_runs[1] != waypoints_across_runs[2])
    v4_pass = (diff_1_2 and diff_2_3 and len(waypoints_across_runs) == 3 and all(w is not None for w in waypoints_across_runs))
    print(f"V4 Pass: {v4_pass} (Run 1 != Run 2: {diff_1_2}, Run 2 != Run 3: {diff_2_3})", flush=True)

asyncio.run(verify_v4())
