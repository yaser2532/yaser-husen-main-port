import asyncio
import math
from playwright.async_api import async_playwright

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))

        print("1. Loading http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await page.wait_for_timeout(600)

        # -------------------------------------------------------------
        # A. Check Sound / Volume Button in Navbar
        # -------------------------------------------------------------
        sound_btn = page.locator("#sound-toggle-btn")
        btn_count = await sound_btn.count()
        print(f"Sound button count in DOM: {btn_count}")
        assert btn_count >= 1, "Sound button (#sound-toggle-btn) must exist in DOM"
        btn_html = await sound_btn.first.inner_html()
        print(f"Sound button HTML: {btn_html}")
        assert "fa-volume-" in btn_html, "Sound button must have FontAwesome volume icon"

        # -------------------------------------------------------------
        # B. Check Galaxy Background & Adaptive Star Canvas
        # -------------------------------------------------------------
        cosmic_bg = page.locator("#cosmic-bg-container")
        bg_style = await cosmic_bg.evaluate("el => getComputedStyle(el).backgroundImage")
        print(f"Cosmic BG Image: {bg_style}")
        assert "galaxy_bg.jpg" in bg_style, "Cosmic background must use galaxy_bg.jpg"

        canvas = page.locator("#cosmic-canvas")
        c_w = await canvas.evaluate("el => el.width")
        c_h = await canvas.evaluate("el => el.height")
        print(f"Cosmic canvas dimensions: {c_w}x{c_h}")
        assert c_w > 0 and c_h > 0, "Cosmic canvas must be initialized with positive dimensions"

        # -------------------------------------------------------------
        # C. Check Dot Elements: Attract & Bounce (NO Clustering)
        # -------------------------------------------------------------
        dots = await page.locator(".mouse-tracker-dot").all()
        print(f"Total dots: {len(dots)}")
        assert len(dots) == 8, f"Expected exactly 8 tracking dots, found {len(dots)}"

        # Move mouse to (600, 400)
        await page.mouse.move(600, 400)
        await page.wait_for_timeout(300)

        # Sample positions over 1.5 seconds to observe oscillation (attract & bounce)
        distances_to_cursor = [[] for _ in range(8)]
        min_pairwise_dists = []

        for sample in range(15):
            coords = []
            for i, dot in enumerate(dots):
                t_str = await dot.evaluate("el => el.style.transform")
                # Parse translate3d(Xrem, Yrem, 0)
                # Or extract client rect
                rect = await dot.evaluate("el => el.getBoundingClientRect()")
                cx = rect["left"] + rect["width"] * 0.5
                cy = rect["top"] + rect["height"] * 0.5
                coords.append((cx, cy))
                dist = math.hypot(cx - 600, cy - 400)
                distances_to_cursor[i].append(dist)

            # Check pairwise distance among dots
            min_pair = 999999
            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    p_dist = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
                    if p_dist < min_pair:
                        min_pair = p_dist
            min_pairwise_dists.append(min_pair)
            await page.wait_for_timeout(100)

        print(f"Min pairwise distance across all samples: {min(min_pairwise_dists):.1f}px")
        # Ensure dots never cluster into a single point
        assert min(min_pairwise_dists) > 12.0, (
            f"Dots clustered too close! Min pairwise distance was {min(min_pairwise_dists):.1f}px"
        )

        for i in range(8):
            d_min = min(distances_to_cursor[i])
            d_max = max(distances_to_cursor[i])
            print(f"Dot #{i}: min dist to cursor={d_min:.1f}px, max dist={d_max:.1f}px, range={d_max - d_min:.1f}px")
            # Must hover around cursor (between 15px and 90px)
            assert 10 <= d_min <= 60, f"Dot #{i} approach distance {d_min}px out of expected range"
            assert 40 <= d_max <= 110, f"Dot #{i} bounce distance {d_max}px out of expected range"

        # -------------------------------------------------------------
        # D. Check Section Pull Timing:
        # Sections down below (e.g. projects, creative-lab) must be pending while near top
        # -------------------------------------------------------------
        projects_sec = page.locator("#projects")
        p_state = await projects_sec.evaluate("el => el.getAttribute('data-nb')")
        print(f"Projects section state at top of page: '{p_state}' (Expected 'pending')")
        assert p_state == "pending", "Projects section must remain pending while visitor is at top of page"

        # Scroll down towards projects
        print("Scrolling smoothly down towards projects...")
        await page.evaluate("window.scrollTo({ top: 1400, behavior: 'smooth' })")
        await page.wait_for_timeout(800)

        p_state_after = await projects_sec.evaluate("el => el.getAttribute('data-nb')")
        print(f"Projects section state after scrolling into view: '{p_state_after}'")

        # Check console errors
        print(f"Console errors collected: {len(errors)}")
        if errors:
            print("Errors:", errors)
        assert len(errors) == 0, f"Expected 0 console errors, got: {errors}"

        await page.screenshot(path="scratch/galaxy_attract_bounce_verified.png")
        print("Screenshot saved to scratch/galaxy_attract_bounce_verified.png")
        await browser.close()
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_verification())
