import asyncio
import math
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))

        print("1. Loading http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await page.wait_for_timeout(600)

        # -------------------------------------------------------------
        # TEST 1: Firefly Dots (White, Red, Theme Gradient Blurry Luminescence)
        # -------------------------------------------------------------
        dots = await page.locator(".mouse-tracker-dot").all()
        print(f"Total firefly dots found: {len(dots)}")
        assert len(dots) == 8, f"Expected 8 dots, found {len(dots)}"

        # Move mouse to (600, 400)
        await page.mouse.move(600, 400)
        await page.wait_for_timeout(600)

        # Check firefly animations
        dot0_anim = await dots[0].evaluate("el => getComputedStyle(el).animationName")
        dot0_shadow = await dots[0].evaluate("el => getComputedStyle(el).boxShadow")
        dot0_filter = await dots[0].evaluate("el => getComputedStyle(el).filter")
        dot0_opacity = await dots[0].evaluate("el => getComputedStyle(el).opacity")
        print(f"Dot #0 animation: {dot0_anim}")
        print(f"Dot #0 box-shadow: {dot0_shadow}")
        print(f"Dot #0 filter: {dot0_filter}")
        print(f"Dot #0 opacity: {dot0_opacity}")

        assert "firefly-color-cycle" in dot0_anim, "Dot must have firefly-color-cycle animation"
        assert "firefly-bioluminescence-blink" in dot0_anim, "Dot must have firefly-bioluminescence-blink animation"
        assert float(dot0_opacity) >= 0.7, "Fireflies must remain brightly luminescent and visible"

        # -------------------------------------------------------------
        # TEST 2: Close Clustering Around Cursor & Continuous Motion when Stationary
        # -------------------------------------------------------------
        # Measure positions of dots at t1
        pos_t1 = await page.evaluate("""() => {
            const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
            return dots.map(d => {
                const r = d.getBoundingClientRect();
                return { x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 };
            });
        }""")

        # Calculate distance to cursor (600, 400)
        distances = [math.hypot(p['x'] - 600, p['y'] - 400) for p in pos_t1]
        max_dist = max(distances)
        avg_dist = sum(distances) / len(distances)
        print(f"Fireflies distance to cursor: avg={avg_dist:.1f}px, max={max_dist:.1f}px")
        assert max_dist < 45, f"Fireflies must be close to cursor! Got max_dist={max_dist:.1f}px"

        # Wait 300ms without moving mouse (stationary cursor)
        await page.wait_for_timeout(300)

        # Measure positions of dots at t2
        pos_t2 = await page.evaluate("""() => {
            const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
            return dots.map(d => {
                const r = d.getBoundingClientRect();
                return { x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 };
            });
        }""")

        # Verify fireflies are constantly in motion even when cursor is stationary
        deltas = [math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y']) for p1, p2 in zip(pos_t1, pos_t2)]
        moving_dots = sum(1 for d in deltas if d > 0.5)
        print(f"Stationary cursor test: {moving_dots}/8 dots in active motion (deltas: {[round(d, 1) for d in deltas]})")
        assert moving_dots == 8, "All 8 fireflies must remain in active motion even when cursor is stationary!"

        # -------------------------------------------------------------
        # TEST 3: Multipurpose Drone Construction in Sequential Interpreter Order
        # -------------------------------------------------------------
        print("\nScrolling halfway into Profile & Expertise...")
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const r = sec.getBoundingClientRect();
            const targetY = window.scrollY + r.top + (r.height * 0.45) - (window.innerHeight * 0.5);
            window.scrollTo({ top: Math.max(0, targetY), behavior: 'instant' });
        }""")
        await page.evaluate("window.dispatchEvent(new Event('scroll'))")

        # Sample at t = 500ms: Title pulling or just assembled, next elements pending
        await page.wait_for_timeout(500)
        sample_500 = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const nodes = window.SectionCoordinator.getNodesForSection('profile-expertise');
            return nodes.map(n => ({
                tag: n.el.tagName,
                cls: n.el.className.slice(0, 20),
                opacity: getComputedStyle(n.el).opacity,
                state: n.state
            }));
        }""")

        print(f"Sample at 500ms ({len(sample_500)} nodes):")
        for i, s in enumerate(sample_500[:4]):
            print(f"  #{i} {s['tag']}.{s['cls']}: opacity={s['opacity']}, state={s['state']}")

        # Title is #0 and actively pulling/assembled
        assert float(sample_500[0]['opacity']) > 0.5, "Title must be pulling first!"
        assert float(sample_500[2]['opacity']) == 0, "Card #1 must be waiting!"

        # Sample at t = 1100ms: Title assembled, paragraph assembled, first box pulling
        await page.wait_for_timeout(600)
        sample_1100 = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const nodes = window.SectionCoordinator.getNodesForSection('profile-expertise');
            return nodes.map(n => ({
                tag: n.el.tagName,
                cls: n.el.className.slice(0, 20),
                opacity: getComputedStyle(n.el).opacity,
                state: n.state
            }));
        }""")
        print(f"Sample at 1100ms:")
        for i, s in enumerate(sample_1100[:4]):
            print(f"  #{i} {s['tag']}.{s['cls']}: opacity={s['opacity']}, state={s['state']}")
        assert sample_1100[0]['state'] == 'assembled', "Title must be assembled"

        # Wait for section construction to complete
        await page.wait_for_timeout(3200)
        sec_state = await page.evaluate("document.getElementById('profile-expertise').getAttribute('data-nb')")
        print(f"Profile-expertise state after construction: {sec_state} (Expected 'built')")
        assert sec_state == "built", "Section should reach built state"

        # -------------------------------------------------------------
        # TEST 4: Drones Reassemble and Cluster Around Cursor After Construction
        # -------------------------------------------------------------
        # Move cursor to (400, 300) and wait 800ms for fireflies to reassemble
        await page.mouse.move(400, 300)
        await page.wait_for_timeout(800)
        re_pos = await page.evaluate("""() => {
            const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
            return dots.map(d => {
                const r = d.getBoundingClientRect();
                return { x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 };
            });
        }""")
        re_dists = [math.hypot(p['x'] - 400, p['y'] - 300) for p in re_pos]
        re_avg = sum(re_dists) / len(re_dists)
        print(f"Post-construction reassembly: avg distance to cursor = {re_avg:.1f}px")
        assert re_avg < 40, f"Drones must reassemble around cursor! Got avg={re_avg:.1f}px"

        # Console error check
        print(f"Console errors: {len(errors)}")
        if errors:
            print("Errors:", errors)
        assert len(errors) == 0, f"Expected 0 errors, got {errors}"

        # Take screenshot of verified state
        await page.screenshot(path="scratch/firefly_verified.png")
        print("Screenshot saved to scratch/firefly_verified.png")

        await browser.close()
        print("\nALL FIREFLY DRONE & SEQUENTIAL INTERPRETER REQUIREMENTS FULLY VERIFIED!")

if __name__ == "__main__":
    asyncio.run(verify())
