import asyncio
from playwright.async_api import async_playwright

SECTIONS = ['home', 'profile-expertise', 'about-me', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact', 'footer']

async def capture_sections():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 375, "height": 812})
        await page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        await asyncio.sleep(1.0)

        # Trigger revealAll to ensure all elements are visible for evaluation
        await page.evaluate("window.drones && window.drones.revealAll && window.drones.revealAll()")
        await asyncio.sleep(0.5)

        for sec_id in SECTIONS:
            sec = await page.query_selector(f"#{sec_id}" if sec_id != 'footer' else "footer")
            if sec:
                await sec.screenshot(path=f"scratch/mobile_sec_{sec_id}.png")
                print(f"Captured scratch/mobile_sec_{sec_id}.png")

        # Test mobile drawer
        menu_toggle = await page.query_selector(".mobile-menu-btn, .menu-toggle, .hamburger, .nav-toggle")
        if menu_toggle:
            print("Found menu toggle:", await menu_toggle.get_attribute("class"))
            await menu_toggle.click()
            await asyncio.sleep(0.4)
            await page.screenshot(path="scratch/mobile_drawer_open.png")
            print("Captured scratch/mobile_drawer_open.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_sections())
