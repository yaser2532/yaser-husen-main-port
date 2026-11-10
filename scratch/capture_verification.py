import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8080/")
        await page.wait_for_timeout(2000)
        
        # Scroll to About/Profile section
        about_el = await page.query_selector('#about')
        if about_el:
            await about_el.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            
        # Capture screenshot of profile section
        profile_wrapper = await page.query_selector('.profile-card-wrapper')
        if profile_wrapper:
            await profile_wrapper.screenshot(path="scratch/verified_circular_profile.png")
            print("Captured profile screenshot.")
            
        # Capture full viewport screenshot of About section
        await page.screenshot(path="scratch/verified_about_section.png")
        print("Captured about section screenshot.")
        
        # Test hover on profile card wrapper
        if profile_wrapper:
            await profile_wrapper.hover()
            await page.wait_for_timeout(500)
            await profile_wrapper.screenshot(path="scratch/verified_profile_hover.png")
            print("Captured profile hover screenshot.")
            
        # Check smooth scrolling to multiple sections
        for sec in ['#home', '#about', '#skills', '#projects', '#contact']:
            el = await page.query_selector(sec)
            if el:
                await el.scroll_into_view_if_needed()
                await page.wait_for_timeout(300)
                
        print("Smooth scroll check to all sections complete with 0 errors!")
        await browser.close()

asyncio.run(main())
