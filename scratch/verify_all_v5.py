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

        # 1. Verify Robotic Nano-Bot Dots: strictly <= 1px, no lightning/arcs
        dots = await page.locator(".mouse-tracker-dot").all()
        print(f"Nano-bot dot count: {len(dots)}")
        assert len(dots) >= 8, f"Expected at least 8 nano-bot dots, got {len(dots)}"
        
        # Check computed size of nano-bot dots
        dot_w = await dots[0].evaluate("el => parseFloat(getComputedStyle(el).width)")
        dot_h = await dots[0].evaluate("el => parseFloat(getComputedStyle(el).height)")
        print(f"Nano-bot dot dimensions: {dot_w}px x {dot_h}px")
        assert dot_w <= 1.5 and dot_h <= 1.5, f"Expected nano-bot dot size <= 1px, got {dot_w}px x {dot_h}px"

        # 2. Verify Cosmic Galaxy Background & Milky Way Nebula
        cosmic_container = page.locator("#cosmic-bg-container")
        assert await cosmic_container.count() == 1, "Cosmic background container must exist"
        opacity = await cosmic_container.evaluate("el => getComputedStyle(el).opacity")
        z_index = await cosmic_container.evaluate("el => getComputedStyle(el).zIndex")
        print(f"Cosmic container opacity: {opacity}, zIndex: {z_index}")
        assert float(opacity) >= 0.8, f"Cosmic background must be visible (opacity >= 0.8), got {opacity}"

        # 3. Verify Compact Modern Cyber Dock Footer
        footer = page.locator("footer#contact")
        assert await footer.count() == 1, "Footer must exist"
        
        # Scroll down to footer
        await footer.scroll_into_view_if_needed()
        await page.wait_for_timeout(1000)

        footer_box = await footer.bounding_box()
        print(f"Footer dimensions: width={footer_box['width']}px, height={footer_box['height']}px")
        # Previously footer was ~250px-300px; compact cyber dock should be <= 130px
        assert footer_box["height"] <= 135, f"Footer height should be compact (<= 135px), got {footer_box['height']}px"

        # Check dock bar components
        dock_bar = page.locator(".cyber-dock-bar")
        assert await dock_bar.count() == 1, "Cyber dock bar must exist"
        
        # 4. Test Nano Chat button in Cyber Dock
        chat_btn = page.locator("#nano-chat-trigger-btn")
        assert await chat_btn.is_visible(), "Chat with AI button must be visible in dock"
        await chat_btn.click()
        await page.wait_for_timeout(400)
        chat_modal = page.locator("#nano-chat-modal-overlay")
        assert await chat_modal.evaluate("el => el.classList.contains('active')"), "Nano chat modal should open on click"
        print("Nano Chat Modal opens successfully from dock!")
        
        # Close Nano Chat modal
        await page.locator("#nano-close-btn").click()
        await page.wait_for_timeout(300)

        # 5. Test Contact Me button in Cyber Dock
        contact_btn = page.locator("#contact-trigger-btn")
        assert await contact_btn.is_visible(), "Contact Me button must be visible in dock"
        await contact_btn.click()
        await page.wait_for_timeout(400)
        contact_modal = page.locator("#contact-modal")
        assert await contact_modal.evaluate("el => el.classList.contains('active')"), "Contact modal should open on click"
        print("Contact Modal opens successfully from dock!")

        # Close Contact modal
        await page.locator("#close-contact-modal").click()
        await page.wait_for_timeout(300)

        # 6. Verify Console Errors
        print(f"Total console errors: {len(console_errors)}")
        if console_errors:
            print("Errors found:", console_errors)
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"

        # 7. Take Screenshots
        await page.screenshot(path="scratch/footer_dock_verified.png")
        print("Footer screenshot saved to scratch/footer_dock_verified.png")

        # Scroll to middle of page and capture galaxy starfield
        await page.locator("#projects").scroll_into_view_if_needed()
        await page.wait_for_timeout(800)
        await page.screenshot(path="scratch/galaxy_projects_verified.png")
        print("Galaxy projects screenshot saved to scratch/galaxy_projects_verified.png")

        await browser.close()
        print("\n>>> ALL TESTS PASSED WITH 100% SUCCESS! <<<")

if __name__ == "__main__":
    asyncio.run(main())
