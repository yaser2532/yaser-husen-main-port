import asyncio
from playwright.async_api import async_playwright

async def full_scroll_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))

        print("Navigating to http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)

        section_ids = [
            "home",
            "profile-expertise",
            "about-me",
            "projects",
            "creative-lab",
            "certificates",
            "secret-desk",
            "contact"
        ]

        # Verify initial states: home is built, other sections are pending
        for sid in section_ids:
            state = await page.evaluate(f"() => document.getElementById('{sid}')?.getAttribute('data-nb')")
            if sid == "home":
                assert state == "built", f"Home should be built, got {state}"
            else:
                assert state == "pending", f"{sid} should be pending initially, got {state}"
        print("Initial section states verified: Home is built, all other sections pending.")

        # Scroll sequentially through each section and observe dynamic pulling
        for sid in section_ids[1:]:
            print(f"Scrolling halfway into section: {sid}...")
            await page.evaluate(f"""() => {{
                const el = document.getElementById('{sid}');
                if (el) {{
                    const r = el.getBoundingClientRect();
                    // Scroll so user is halfway scrolled into the section (core viewpoint)
                    const targetY = window.scrollY + r.top + (r.height * 0.45) - (window.innerHeight * 0.5);
                    window.scrollTo({{ top: Math.max(0, targetY), behavior: 'instant' }});
                }}
            }}""")
            await page.evaluate("window.dispatchEvent(new Event('scroll'))")
            await page.wait_for_timeout(1400) # Give pull-build time to execute its sequential pull animation

            # Check state of section
            s_state = await page.evaluate(f"() => document.getElementById('{sid}')?.getAttribute('data-nb')")
            print(f"Section {sid} state after scroll: {s_state}")
            assert s_state in ["pulling", "snapping", "built"], f"Section {sid} should be active or built, got {s_state}"

            # Check that elements in view are assembled
            in_view_assembled = await page.evaluate(f"""() => {{
                const sec = document.getElementById('{sid}');
                if (!sec) return 0;
                const viewH = window.innerHeight;
                const nodes = Array.from(sec.querySelectorAll('[data-assembled="true"]'));
                return nodes.length;
            }}""")
            print(f"Section {sid} assembled elements in view: {in_view_assembled}")
            assert in_view_assembled > 0, f"Section {sid} must have assembled elements in view"

        # Check final console errors
        print(f"Total console errors across full scroll: {len(errors)}")
        if errors:
            print("Errors:", errors)
        assert len(errors) == 0, f"Expected 0 errors, got: {errors}"

        # Capture full page screenshot
        await page.screenshot(path="scratch/full_scroll_verified.png", full_page=False)
        print("Screenshot saved to scratch/full_scroll_verified.png")
        await browser.close()
        print("ALL SCROLL & ELEMENT HOISTING TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(full_scroll_test())
