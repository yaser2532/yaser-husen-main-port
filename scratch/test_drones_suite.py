import asyncio
import time
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        errors = []
        page.on('console', lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type == 'error' else None)
        page.on('pageerror', lambda err: errors.append(f"PAGEERROR: {err}"))
        
        print("Navigating to http://localhost:8080/ ...")
        t0 = time.time()
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        # V1: Load timing check at 100ms, 500ms, 1500ms, 3000ms
        await page.screenshot(path='scratch/v1_load_100ms.png')
        await page.wait_for_timeout(400)
        await page.screenshot(path='scratch/v1_load_500ms.png')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/v1_load_1500ms.png')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/v1_load_3000ms.png')
        print("Captured V1 load screenshots.")
        
        # Check drone counts and properties
        drone_info = await page.evaluate('''() => {
            if (!window.drones) return null;
            const ds = window.drones.getDrones();
            const els = window.drones.getElements();
            return {
                dronesCount: ds.length,
                states: ds.map(d => d.state),
                rMin: window.drones.R_MIN,
                rMax: window.drones.R_MAX,
                elementsCount: els.length,
                pendingCount: els.filter(e => e.state === 'pending').length,
                builtCount: els.filter(e => e.state === 'built').length
            };
        }''')
        print("Drone Info:", drone_info)
        
        # V6: Cursor Follow test (move mouse to 6 points, sample frames)
        points = [
            (300, 200), (800, 250), (1200, 300),
            (200, 600), (700, 500), (1100, 700)
        ]
        
        follow_results = []
        for x, y in points:
            await page.mouse.move(x, y)
            await page.wait_for_timeout(450)
            dist_check = await page.evaluate('''(pt) => {
                const ds = window.drones.getDrones();
                const dists = ds.map(d => Math.hypot(d.x - pt.x, d.y - pt.y));
                const maxDist = Math.max(...dists);
                return { maxDist, allWithinRmax: maxDist <= (window.drones.R_MAX + 10) };
            }''', {'x': x, 'y': y})
            follow_results.append(dist_check)
            
        print("Follow Results:", follow_results)
        
        # V2: DIM test (hover h1, check opacity)
        h1 = await page.query_selector('.hero-title')
        if h1:
            box = await h1.bounding_box()
            await page.mouse.move(box['x'] + 50, box['y'] + box['height'] / 2)
            await page.wait_for_timeout(250)
            dim_info = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                const opacities = ds.map(d => d.opacity);
                const avgOp = opacities.reduce((a, b) => a + b, 0) / opacities.length;
                return { avgOp, opacities: opacities.slice(0, 4) };
            }''')
            print("DIM over text Info:", dim_info)
            
            # Move off text to empty space
            await page.mouse.move(100, 100)
            await page.wait_for_timeout(350)
            restore_info = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                const opacities = ds.map(d => d.opacity);
                const avgOp = opacities.reduce((a, b) => a + b, 0) / opacities.length;
                return { avgOp, opacities: opacities.slice(0, 4) };
            }''')
            print("Restore off text Info:", restore_info)
            
        # V7: Scroll test to Expertise & Projects
        print("Testing scroll to profile-expertise...")
        await page.evaluate("window.scrollTo({ top: 600, behavior: 'smooth' })")
        await page.wait_for_timeout(1200)
        await page.screenshot(path='scratch/scroll_expertise_building.png')
        await page.wait_for_timeout(1800)
        await page.screenshot(path='scratch/scroll_expertise_built.png')
        
        print("Errors captured:", errors)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
