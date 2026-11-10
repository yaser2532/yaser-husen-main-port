import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))
        
        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        # 1. Smoothly scroll toward About Me to trigger the drone pulling sequence
        print("Scrolling to About Me section...")
        await page.evaluate("""() => {
            const el = document.querySelector('#about-me');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        }""")
        
        # Sample mid-pull (drone in flight / pulling with tractor beams)
        await page.wait_for_timeout(550)
        mid_pull_shot = os.path.join(ARTIFACT_DIR, 'cinematic_drone_pulling_live.png')
        await page.screenshot(path=mid_pull_shot)
        print("Saved cinematic_drone_pulling_live.png!")
        
        # Sample when code block is actively being pulled or finished
        await page.wait_for_timeout(1200)
        about_shot = os.path.join(ARTIFACT_DIR, 'cinematic_about_code_block.png')
        await page.screenshot(path=about_shot)
        print("Saved cinematic_about_code_block.png!")
        
        # Check code block terminal element alone
        cb = await page.query_selector('.code-block-visual')
        if cb:
            cb_shot = os.path.join(ARTIFACT_DIR, 'balanced_code_terminal_detail.png')
            await cb.screenshot(path=cb_shot)
            print("Saved balanced_code_terminal_detail.png!")
            
        # Inspect state of elements
        states = await page.evaluate("""() => {
            const els = window.drones.getElements();
            const byState = {};
            els.forEach(e => {
                byState[e.state] = (byState[e.state] || 0) + 1;
            });
            return byState;
        }""")
        print("Element states at current point:", states)
        
        # Test scroll through rest of page
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1500)
        
        final_states = await page.evaluate("""() => {
            const els = window.drones.getElements();
            return {
                total: els.length,
                built: els.filter(e => e.state === 'built').length,
                pending: els.filter(e => e.state === 'pending').length
            };
        }""")
        print("Final states at footer:", final_states)
        
        # Check responsive overflow across all 6 viewports
        viewports = [320, 375, 768, 1024, 1440, 2560]
        overflows = {}
        for vp in viewports:
            await page.set_viewport_size({'width': vp, 'height': 800})
            await page.wait_for_timeout(120)
            sw, cw = await page.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
            overflows[vp] = max(0, sw - cw)
            
        print("Responsive overflows:", overflows)
        print("Console errors:", console_errors)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
