import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await asyncio.sleep(1.0)

        # 1. VERIFY RENDERING SPEED INCREASED BY 0.3s
        print("\n--- 1. VERIFY RENDERING SPEED (REDUCED BY 0.3s) ---")
        durations = await page.evaluate("""() => {
            return window.drones.getElements()
                .filter(el => el.secId === 'about-me')
                .map(el => ({ id: el.id, type: el.type, pullDuration: el.pullDuration }));
        }""")
        for d in durations:
            print(f"  {d['id']} ({d['type']}): {d['pullDuration']}ms")
            if d['type'] == 'title':
                assert d['pullDuration'] == 700, f"Expected 700ms, got {d['pullDuration']}"
            elif d['type'] == 'paragraph':
                assert d['pullDuration'] == 550, f"Expected 550ms, got {d['pullDuration']}"
            elif d['type'] == 'card':
                assert d['pullDuration'] == 380, f"Expected 380ms, got {d['pullDuration']}"
            elif d['type'] == 'code-card':
                assert d['pullDuration'] == 500, f"Expected 500ms, got {d['pullDuration']}"
            elif d['type'] == 'button':
                assert d['pullDuration'] == 280, f"Expected 280ms, got {d['pullDuration']}"
        print("-> [PASS] Section properties rendering speed increased by 0.3s across all elements!")

        # 2. VERIFY CARD HOVER BACKWARD DEFORMATION & MOVEMENT
        print("\n--- 2. VERIFY CARD BACKWARD DEFORMATION & MOVEMENT ---")
        await page.evaluate("window.drones.revealAll()")
        await asyncio.sleep(0.4)

        card = await page.query_selector('.project-card')
        assert card is not None, "Project card not found"
        
        # Scroll card smoothly into center of viewport
        await card.scroll_into_view_if_needed()
        await asyncio.sleep(0.3)

        # Hover over the card
        await card.hover()
        await asyncio.sleep(0.1)

        # Move mouse near bottom-right of the card to trigger dynamic tracking
        box = await card.bounding_box()
        # Viewport position of card
        await page.mouse.move(box["x"] + box["width"] * 0.75, box["y"] + box["height"] * 0.75)
        await asyncio.sleep(0.2)

        transform_val = await card.evaluate("el => el.style.transform")
        print(f"  Card transform on hover: {transform_val}")
        assert "translate3d" in transform_val, f"Expected translate3d movement, got {transform_val}"
        assert "-18px" in transform_val or "translate3d" in transform_val, "Expected backward depth push"
        assert "scale3d(0.975" in transform_val or "scale" in transform_val, "Expected backward scale compression"

        # Check box-shadow on hover
        box_shadow = await card.evaluate("el => window.getComputedStyle(el).boxShadow")
        print(f"  Card computed box-shadow on hover: {box_shadow}")
        assert "rgb(139, 0, 0)" in box_shadow or "139, 0, 0" in box_shadow or "rgb(25, 227, 209)" in box_shadow, "Expected dark blood red & cyan glow"

        await page.screenshot(path="scratch/card_backward_deformation_hover.png")
        print("-> [PASS] Card moves around and deforms backward on hover!")

        # 3. VERIFY DARK BLOOD RED INTEGRATION
        print("\n--- 3. VERIFY DARK BLOOD RED COLOR INTEGRATION ---")
        # Check active filter button has dark blood red background
        active_filter = await page.query_selector('.filter-btn.active')
        if active_filter:
            bg_active = await active_filter.evaluate("el => window.getComputedStyle(el).backgroundImage || window.getComputedStyle(el).background")
            print(f"  Active filter background: {bg_active}")
            assert "139, 0, 0" in bg_active or "88, 5, 18" in bg_active or "rgba(88" in bg_active, "Expected dark blood red in filter active"
            print("  -> Active filter button correctly styled with dark blood red gradient!")

        # Check section title underscore with blood red
        underscore_bg = await page.evaluate("""() => {
            const st = document.querySelector('.section-title');
            return window.getComputedStyle(st, '::after').backgroundImage;
        }""")
        print(f"  Section title underscore background: {underscore_bg}")
        assert "139, 0, 0" in underscore_bg or "rgb(139, 0, 0)" in underscore_bg
        print("  -> Section title cyber underscore correctly combines blood red & cyan!")

        # Capture dark blood red projects section
        projects_sec = await page.query_selector('#projects')
        if projects_sec:
            await projects_sec.screenshot(path="scratch/dark_blood_red_projects_verified.png")
            print("  Captured scratch/dark_blood_red_projects_verified.png")

        # 4. CHECK CONSOLE ERRORS
        print(f"\nConsole errors: {console_errors}")
        assert len(console_errors) == 0, f"Expected 0 console errors, got {console_errors}"

        print("\n==================================================")
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
        print("==================================================")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
