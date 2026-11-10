import asyncio
from playwright.async_api import async_playwright

async def run_full_suite():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        errors = []
        page.on('console', lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page.on('pageerror', lambda err: errors.append(f"PAGEERROR: {err}"))
        
        print("Navigating to http://localhost:8080/ ...")
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(2500)
        
        sections = [
            ("profile-expertise", "scratch/section_expertise.png"),
            ("about", "scratch/section_about.png"),
            ("projects", "scratch/section_projects.png"),
            ("creative-lab", "scratch/section_creativelab.png"),
            ("certificates", "scratch/section_certificates.png"),
            ("secret-desk", "scratch/section_secretdesk.png"),
            ("contact", "scratch/section_contact.png")
        ]
        
        for sec_id, img_path in sections:
            sec_el = await page.query_selector(f'#{sec_id}')
            if sec_el:
                print(f"Scrolling to section #{sec_id}...")
                await sec_el.scroll_into_view_if_needed()
                # Simulate mouse hovering over section to trigger drone pull
                rect = await sec_el.bounding_box()
                if rect:
                    mid_x = rect['x'] + rect['width'] / 2
                    mid_y = rect['y'] + min(rect['height'] / 2, 400)
                    await page.mouse.move(mid_x, mid_y)
                
                # Wait for sequential pull animation
                await page.wait_for_timeout(1800)
                await page.screenshot(path=img_path)
                print(f"Saved {img_path}")
            else:
                print(f"Warning: Section #{sec_id} not found!")

        # Scroll to bottom / footer
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1500)
        await page.screenshot(path="scratch/section_footer.png")
        print("Saved scratch/section_footer.png")
        
        # Test mobile viewport 375x812
        print("Testing mobile viewport 375x812...")
        await page.set_viewport_size({'width': 375, 'height': 812})
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/mobile_hero.png")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/mobile_footer.png")
        print("Saved mobile screenshots")
        
        print("\n--- RESULTS ---")
        print(f"Total Errors Captured: {len(errors)}")
        for err in errors:
            print("  ", err)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run_full_suite())
