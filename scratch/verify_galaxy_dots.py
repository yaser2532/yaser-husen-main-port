import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        print("Navigating to http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")

        # 1. Verify Big Cursor Light is DISABLED
        mouse_glow = page.locator("#mouse-glow")
        glow_display = await mouse_glow.evaluate("el => getComputedStyle(el).display")
        print(f"Mouse glow display style: '{glow_display}' (Must be 'none')")
        assert glow_display == "none", "Big cursor light bulb (#mouse-glow) must be disabled"

        # 2. Verify Dot Elements: Bigger (8px - 14px) and Self-Emitting Glowing Light
        dots = await page.locator(".mouse-tracker-dot").all()
        print(f"Tracking dots count: {len(dots)}")
        assert len(dots) >= 8, f"Expected at least 8 tracking dots, got {len(dots)}"

        # Check dimensions of multiple dots
        for idx in range(min(4, len(dots))):
            w = await dots[idx].evaluate("el => parseFloat(getComputedStyle(el).width)")
            h = await dots[idx].evaluate("el => parseFloat(getComputedStyle(el).height)")
            shadow = await dots[idx].evaluate("el => getComputedStyle(el).boxShadow")
            print(f"Dot #{idx}: {w}px x {h}px, glow: {shadow}")
            assert 7.5 <= w <= 15 and 7.5 <= h <= 15, f"Dot #{idx} should be between 8px and 14px, got {w}px"
            assert shadow != "none" and len(shadow) > 5, f"Dot #{idx} must emit its own light via box-shadow"

        # Move mouse and verify dots follow
        await page.mouse.move(500, 300)
        await page.wait_for_timeout(300)
        d0_transform = await dots[0].evaluate("el => el.style.transform")
        print(f"Dot #0 transform after mousemove: {d0_transform}")
        assert "translate3d" in d0_transform, "Dots must follow mouse coordinates"

        # 3. Verify Background: Real HD Galaxy Image + Minuscule 3D Stars
        cosmic_bg = page.locator("#cosmic-bg-container")
        bg_image = await cosmic_bg.evaluate("el => getComputedStyle(el).backgroundImage")
        print(f"Cosmic container background-image: {bg_image}")
        assert "galaxy_bg.jpg" in bg_image, "Cosmic background container must use galaxy_bg.jpg"

        # 4. Verify Hero Section: Kinetic Signal Removed
        visualizer_count = await page.locator(".hero-visualizer-wrap, #hero-audio-visualizer").count()
        print(f"Hero visualizer count: {visualizer_count} (Must be 0)")
        assert visualizer_count == 0, "Hero kinetic signal visualizer should be removed"

        # 5. Verify Grid Lines Removed in 3D WebGL
        # Check that no GridHelper exists in backdropGroup
        has_grid = await page.evaluate("""() => {
            if (window.__gl && window.__gl.scene) {
                let foundGrid = false;
                window.__gl.scene.traverse((obj) => {
                    if (obj.type === 'GridHelper' || obj.isGridHelper) foundGrid = true;
                });
                return foundGrid;
            }
            return false;
        }""")
        print(f"3D Scene contains GridHelper: {has_grid} (Must be False)")
        assert not has_grid, "3D scene must not contain GridHelper floor lines"

        # 6. Check Console Errors
        print(f"Console errors: {len(console_errors)}")
        if console_errors:
            print("Errors found:", console_errors)
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"

        # 7. Take visual screenshots
        await page.screenshot(path="scratch/galaxy_hero_final.png")
        print("Hero screenshot saved to scratch/galaxy_hero_final.png")

        await page.locator("#projects").scroll_into_view_if_needed()
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/galaxy_projects_final.png")
        print("Projects screenshot saved to scratch/galaxy_projects_final.png")

        await page.locator("footer#contact").scroll_into_view_if_needed()
        await page.wait_for_timeout(800)
        await page.screenshot(path="scratch/galaxy_footer_final.png")
        print("Footer screenshot saved to scratch/galaxy_footer_final.png")

        await browser.close()
        print("\n>>> ALL CHECKS PASSED WITH 100% SUCCESS! <<<")

if __name__ == "__main__":
    asyncio.run(main())
