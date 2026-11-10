import asyncio
import time
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await asyncio.sleep(0.5)

        # 1. Check irregular sizes
        drone_sizes = await page.evaluate("window.drones.getDrones().map(d => d.size)")
        print(f"Drone sizes count: {len(drone_sizes)}")
        print(f"Sample drone sizes: {drone_sizes[:10]}")
        unique_sizes = sorted(list(set(drone_sizes)))
        print(f"Unique irregular sizes: {unique_sizes}")
        assert len(unique_sizes) >= 6, f"Expected irregular sizes, got {unique_sizes}"

        # 2. Check tails removed
        trail_counts = await page.evaluate("window.drones.getDrones().map(d => d.trailCount)")
        print(f"Drone trailCounts: {set(trail_counts)}")
        assert all(c == 0 for c in trail_counts), f"Expected 0 trail counts, got {trail_counts}"

        # 3. Check pull durations configured in elementList
        element_configs = await page.evaluate("""() => {
            return window.drones.getElements()
                .filter(el => el.secId === 'about-me')
                .map(el => ({ id: el.id, type: el.type, pullDuration: el.pullDuration }));
        }""")
        print("\nAbout section registered elements and configured pull durations:")
        for ec in element_configs:
            print(f"  {ec['id']} ({ec['type']}): {ec['pullDuration']}ms")

        # Verify each expected pull duration (+300ms)
        for ec in element_configs:
            if ec['type'] == 'title':
                assert ec['pullDuration'] == 1000, f"Expected 1000ms title pull, got {ec['pullDuration']}"
            elif ec['type'] == 'paragraph':
                assert ec['pullDuration'] == 850, f"Expected 850ms paragraph pull, got {ec['pullDuration']}"
            elif ec['type'] == 'code-card':
                assert ec['pullDuration'] == 800, f"Expected 800ms code-card pull, got {ec['pullDuration']}"
            elif ec['type'] == 'button':
                assert ec['pullDuration'] == 580, f"Expected 580ms button pull, got {ec['pullDuration']}"
            elif ec['type'] == 'card':
                assert ec['pullDuration'] == 680, f"Expected 680ms card pull, got {ec['pullDuration']}"

        # 4. Scroll smoothly to About section and monitor sequential execution
        print("\nScrolling into About section to monitor sequential build...")
        await page.evaluate("""() => {
            const sec = document.getElementById('about-me');
            sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }""")

        # Poll activeMissions and element states every 25ms for 6.5 seconds
        history = []
        max_active_missions = 0
        t0 = time.time()
        
        while time.time() - t0 < 6.5:
            now_rel = round((time.time() - t0) * 1000)
            data = await page.evaluate("""() => {
                const missions = window.drones.getMissions();
                const aboutEls = window.drones.getElements().filter(e => e.secId === 'about-me');
                return {
                    activeCount: missions.length,
                    activeItemId: missions.length > 0 ? missions[0].item.id : null,
                    activeItemType: missions.length > 0 ? missions[0].item.type : null,
                    states: aboutEls.map(e => ({ id: e.id, type: e.type, state: e.state }))
                };
            }""")
            if data["activeCount"] > max_active_missions:
                max_active_missions = data["activeCount"]
            
            history.append((now_rel, data["activeCount"], data["activeItemId"]))
            await asyncio.sleep(0.025)

        print(f"\nMaximum concurrent active missions observed: {max_active_missions}")
        assert max_active_missions <= 1, f"Expected strictly sequential (<=1) active missions, observed {max_active_missions}"

        # Analyze timeline of element builds
        print("\nElement state log through timeline:")
        last_item = None
        for now_rel, count, item_id in history:
            if item_id != last_item:
                print(f"  t={now_rel}ms: active mission item -> {item_id}")
                last_item = item_id

        # Verify all elements in about-me finished as 'built'
        final_about_states = await page.evaluate("""() => {
            return window.drones.getElements()
                .filter(e => e.secId === 'about-me')
                .map(e => ({ id: e.id, type: e.type, state: e.state }));
        }""")
        print("\nFinal About-me element states:")
        for s in final_about_states:
            print(f"  {s['id']} ({s['type']}): {s['state']}")
            assert s['state'] == 'built', f"Element {s['id']} was not built: {s['state']}"

        # 5. Capture screenshot of rendered About section
        await page.screenshot(path="scratch/about_sequential_verified.png")
        print("\nScreenshot saved to scratch/about_sequential_verified.png")

        # 6. Check console errors
        print(f"Console errors: {console_errors}")
        assert len(console_errors) == 0, f"Expected 0 console errors, got {console_errors}"

        print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
