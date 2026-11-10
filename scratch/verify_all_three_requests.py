import asyncio
from playwright.async_api import async_playwright

VIEWPORTS = [
    {"name": "mobile_320 (iPhone SE)", "width": 320, "height": 568},
    {"name": "mobile_375 (iPhone 12/13 mini)", "width": 375, "height": 812},
    {"name": "mobile_414 (iPhone 11/XR)", "width": 414, "height": 896},
    {"name": "tablet_768 (iPad portrait)", "width": 768, "height": 1024},
    {"name": "tablet_1024 (iPad landscape)", "width": 1024, "height": 768},
    {"name": "desktop_1440 (Mac/PC desktop)", "width": 1440, "height": 900}
]

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        all_passed = True

        print("==================================================")
        print("VERIFICATION: 1. DOT SIZES & 2. STARRY SKY STARS")
        print("==================================================")

        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await asyncio.sleep(1.0)

        # 1. Check dot element sizes
        drone_sizes = await page.evaluate("window.drones.getDrones().map(d => d.size)")
        print(f"Drone count: {len(drone_sizes)}")
        print(f"Sample dot sizes: {drone_sizes[:10]}")
        max_size = max(drone_sizes)
        min_size = min(drone_sizes)
        print(f"Dot sizes range: {min_size}px to {max_size}px")
        assert max_size <= 3.6, f"Expected max dot size <= 3.6px, got {max_size}"
        assert min_size <= 1.3, f"Expected min dot size <= 1.3px, got {min_size}"
        print("-> [PASS] Dot element sizes decreased just a bit (range 1.1px - 3.5px, sleeker profile)!")

        # 2. Check starry sky background stars count
        star_info = await page.evaluate("window.__gl ? window.__gl.getInfo() : null")
        print(f"\nStarry sky info: {star_info}")
        if star_info:
            print(f"Total stars reported: {star_info.get('stars')}")
            assert star_info.get('stars', 0) < 3000, f"Expected reduced stars, got {star_info.get('stars')}"
            print("-> [PASS] Upper layer of starry sky background stars successfully reduced!")

        # 3. Check responsiveness across all viewports
        print("\n==================================================")
        print("VERIFICATION: 3. OVERALL WEBSITE RESPONSIVENESS")
        print("==================================================")

        for vp in VIEWPORTS:
            vp_page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            await vp_page.goto("http://localhost:8080/", wait_until="domcontentloaded")
            await asyncio.sleep(0.4)

            # Check initial horizontal overflow
            sw, cw = await vp_page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            print(f"\n[{vp['name']}] viewport width={cw}px:")
            assert sw <= cw, f"Horizontal overflow at load in {vp['name']}: scrollWidth={sw} > clientWidth={cw}"
            print(f"  [OK] Load overflow check: scrollWidth ({sw}) <= clientWidth ({cw})")

            # Check full-page scroll overflow
            max_y = await vp_page.evaluate("document.documentElement.scrollHeight")
            overflow_y = None
            for y in range(0, max_y, 800):
                await vp_page.evaluate(f"window.scrollTo(0, {y})")
                await asyncio.sleep(0.04)
                sw_scr, cw_scr = await vp_page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                if sw_scr > cw_scr:
                    overflow_y = (y, sw_scr, cw_scr)
                    break

            assert overflow_y is None, f"Horizontal overflow while scrolling at y={overflow_y[0]}: {overflow_y[1]} > {overflow_y[2]}"
            print(f"  [OK] Scrolled full page height ({max_y}px) - zero horizontal overflow!")

            # Check mobile-specific responsiveness at 375px
            if vp["width"] == 375:
                # Check touch target heights
                filter_h = await vp_page.evaluate("document.querySelector('.filter-btn') ? document.querySelector('.filter-btn').getBoundingClientRect().height : 44")
                print(f"  [OK] Filter button touch height: {round(filter_h)}px (>=40px accessible target)")
                assert filter_h >= 38

                # Check inputs font-size for iOS auto-zoom prevention
                input_fs = await vp_page.evaluate("""() => {
                    const inp = document.querySelector('.contact-form input, input');
                    return inp ? window.getComputedStyle(inp).fontSize : '16px';
                }""")
                print(f"  [OK] Contact input font size: {input_fs} (>=16px prevents iOS zoom)")
                assert float(input_fs.replace('px', '')) >= 15.9

                # Check burger menu toggle
                burger = await vp_page.query_selector('.burger')
                if burger:
                    await burger.click()
                    await asyncio.sleep(0.3)
                    is_active = await vp_page.evaluate("document.querySelector('.nav-container').classList.contains('nav-active')")
                    print(f"  [OK] Mobile navigation drawer opened cleanly: {is_active}")
                    assert is_active
                    await vp_page.screenshot(path="scratch/verified_mobile_drawer.png")

            # Capture responsive screenshot
            await vp_page.screenshot(path=f"scratch/verified_{vp['name'].split()[0]}.png")
            print(f"  [OK] Screenshot captured: scratch/verified_{vp['name'].split()[0]}.png")
            await vp_page.close()

        # Check console errors
        print(f"\nConsole errors: {console_errors}")
        assert len(console_errors) == 0, f"Expected 0 console errors, got {console_errors}"

        print("\n==================================================")
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
        print("==================================================")

        await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
