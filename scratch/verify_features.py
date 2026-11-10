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

        # 1. Check UTC Clock
        clock_text = await page.inner_text("#clock-utc")
        print(f"Clock text: '{clock_text}'")
        assert "UTC " in clock_text, f"Unexpected clock text: {clock_text}"

        # 2. Check Audio-Reactive Visualizer Bars
        v_bars = await page.locator(".hero-audio-visualizer .v-bar").all()
        print(f"Visualizer bars count: {len(v_bars)}")
        assert len(v_bars) == 16, f"Expected 16 visualizer bars, got {len(v_bars)}"

        # Measure bar heights after 400ms
        await page.wait_for_timeout(400)
        h1 = await v_bars[0].evaluate("el => el.offsetHeight")
        h5 = await v_bars[4].evaluate("el => el.offsetHeight")
        print(f"Sample bar heights: bar[0]={h1}px, bar[4]={h5}px")
        assert h1 >= 3 and h5 >= 3, "Visualizer bars should have rendered height >= 3"

        # 3. Check 3D Hero Name & typing
        # Wait up to 3 seconds for typing to complete and split into 3D chars
        await page.wait_for_timeout(2500)
        chars = await page.locator(".hero-3d-char").all()
        print(f"3D hero characters count: {len(chars)}")
        assert len(chars) >= 10, f"Expected at least 10 3D characters for 'YASER HUSEN', got {len(chars)}"

        # Hover near the first char
        box = await chars[0].bounding_box()
        if box:
            await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            await page.wait_for_timeout(200)
            is_repelled = await chars[0].evaluate("el => el.classList.contains('is-repelled')")
            print(f"First 3D char repulsion active on hover: {is_repelled}")

        # 4. Check Filter Buttons styling and count
        filter_btns = await page.locator(".filter-btn").all()
        print(f"Filter buttons count: {len(filter_btns)}")
        assert len(filter_btns) == 4, f"Expected 4 filter buttons, got {len(filter_btns)}"
        btn_texts = [await b.inner_text() for b in filter_btns]
        print(f"Filter buttons: {btn_texts}")
        assert "All Projects" in btn_texts[0]
        assert "AI & Data Science" in btn_texts[1]
        assert "Web Apps" in btn_texts[2]
        assert "Creative Labs" in btn_texts[3]

        # 5. Check Project Cards 3D Parallax Tilt
        cards = await page.locator(".project-card").all()
        print(f"Project cards count: {len(cards)}")
        assert len(cards) > 0, "No project cards found"
        
        # Scroll project card into view first so mouse coordinates hit it
        await cards[0].scroll_into_view_if_needed()
        await page.wait_for_timeout(400)
        card_box = await cards[0].bounding_box()
        if card_box:
            # Move mouse over card offset
            await page.mouse.move(card_box["x"] + card_box["width"] * 0.75, card_box["y"] + card_box["height"] * 0.75)
            await page.wait_for_timeout(300)
            tilt_x = await cards[0].evaluate("el => el.style.getPropertyValue('--tilt-x') || getComputedStyle(el).getPropertyValue('--tilt-x')")
            tilt_y = await cards[0].evaluate("el => el.style.getPropertyValue('--tilt-y') || getComputedStyle(el).getPropertyValue('--tilt-y')")
            print(f"Project card 3D tilt styles: --tilt-x={tilt_x.strip()}, --tilt-y={tilt_y.strip()}")
            assert len(tilt_x.strip()) > 0 and float(tilt_x.strip()) != 0, f"Card --tilt-x should be non-zero on mouse hover, got '{tilt_x}'"

        # 6. Check Firefly Swarm & Canvas
        canvas = await page.locator("#nb-canvas").count()
        print(f"Blueprint/swarm canvas count: {canvas}")
        assert canvas == 1, "Blueprint/swarm canvas should exist"

        # 7. Check Cosmic Sky container
        cosmic = await page.locator("#cosmic-bg-container").count()
        print(f"Cosmic sky container count: {cosmic}")
        assert cosmic == 1, "Cosmic sky container should exist"

        # 8. Check Lamp Physics and toggle
        lamp_arm = await page.locator("#lamp-swing-arm").count()
        print(f"Lamp arm count: {lamp_arm}")
        assert lamp_arm == 1, "Lamp arm should exist"

        # Check console errors
        print("Console errors count:", len(console_errors))
        if console_errors:
            print("Errors:", console_errors)
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"

        # Take a visual screenshot of the Hero page
        await page.screenshot(path="scratch/hero_verified.png")
        print("Screenshot saved to scratch/hero_verified.png")

        # Scroll down to Projects and take screenshot
        await page.locator("#projects").scroll_into_view_if_needed()
        await page.wait_for_timeout(1200)
        await page.screenshot(path="scratch/projects_verified.png")
        print("Screenshot saved to scratch/projects_verified.png")

        await browser.close()
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
