import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

async def test_and_capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))
        
        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        # 1. Capture About Me Code Block Visual (Red & Black)
        about_el = await page.query_selector('#about-me')
        if about_el:
            await about_el.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            cb = await page.query_selector('.code-block-visual')
            if cb:
                await cb.screenshot(path=os.path.join(ARTIFACT_DIR, 'red_black_code_terminal.png'))
                print("Saved red_black_code_terminal.png!")
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'red_black_about_section.png'))
            print("Saved red_black_about_section.png!")
        
        # 2. Capture Featured Projects with Dark Blood Red filters & badges
        proj_el = await page.query_selector('#projects')
        if proj_el:
            await proj_el.scroll_into_view_if_needed()
            await page.wait_for_timeout(800)
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'dark_blood_red_projects.png'))
            print("Saved dark_blood_red_projects.png!")
            
        # 3. Check responsive overflow across all 6 viewports
        viewports = [320, 375, 768, 1024, 1440, 2560]
        overflows = {}
        for vp in viewports:
            await page.set_viewport_size({'width': vp, 'height': 800})
            await page.wait_for_timeout(150)
            sw, cw = await page.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
            overflow = max(0, sw - cw)
            overflows[vp] = overflow
            print(f"Viewport {vp}px: overflow = {overflow}px")
            
        print("Console errors:", console_errors)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_and_capture())
