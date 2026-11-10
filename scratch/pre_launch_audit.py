import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        console_errors = []
        page.on('console', lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(f"[pageerror] {str(err)}"))

        print("1. Loading website at http://localhost:8080/ ...")
        res = await page.goto("http://localhost:8080/", wait_until='networkidle')
        assert res.status == 200, f"Expected HTTP 200, got {res.status}"
        print(f"   HTTP Status: {res.status} OK")

        # 2. Check Hero
        print("\n2. Checking Hero Section...")
        hero_title = await page.evaluate("() => document.querySelector('.hero-title').innerText")
        print(f"   Hero Title text: '{hero_title.strip()}'")
        assert 'YASER HUSEN' in hero_title.upper(), "Hero title must contain YASER HUSEN"

        # 3. Check About Me & Code Block Visual
        print("\n3. Checking About Me & Code Block Visual...")
        await page.evaluate("document.getElementById('about-me').scrollIntoView()")
        await page.wait_for_timeout(600)
        code_info = await page.evaluate('''() => {
            const cb = document.querySelector('.code-block-visual');
            const lines = Array.from(cb.querySelectorAll('.drone-code-line'));
            return {
                exists: !!cb,
                opacity: parseFloat(window.getComputedStyle(cb).opacity),
                title: cb.querySelector('.terminal-filename') ? cb.querySelector('.terminal-filename').innerText : '',
                linesCount: lines.length,
                allLinesVisible: lines.every(l => window.getComputedStyle(l).clipPath.includes('0px')),
                firstLine: lines[0] ? lines[0].innerText : ''
            };
        }''')
        print(f"   Code Block Visual: exists={code_info['exists']}, opacity={code_info['opacity']}")
        print(f"   Terminal Title: {code_info['title']}, Lines: {code_info['linesCount']}")
        print(f"   All Lines Visible: {code_info['allLinesVisible']}")
        assert code_info['exists'], "Code block visual must exist"
        assert code_info['opacity'] >= 0.75, f"Code block must be visible, got opacity {code_info['opacity']}"
        assert code_info['linesCount'] == 10, f"Expected 10 code lines, got {code_info['linesCount']}"
        assert code_info['allLinesVisible'], "All 10 code lines must be unclipped and visible"

        # 4. Check Drone Dots Size & Performance
        print("\n4. Checking Drone Dots & Refined Sizes...")
        drone_sizes = await page.evaluate("() => window.drones.getDrones().map(d => d.size)")
        print(f"   Drones count: {len(drone_sizes)}, Min size: {min(drone_sizes):.2f}px, Max size: {max(drone_sizes):.2f}px")
        assert max(drone_sizes) <= 4.0, f"Drones should be smaller (max <= 4.0px), got {max(drone_sizes)}"
        assert min(drone_sizes) >= 2.0, f"Drones should be legible (min >= 2.0px), got {min(drone_sizes)}"

        # 5. Check Section Pulls & Complete Scroll to Bottom
        print("\n5. Testing Scroll Through All Sections to Bottom...")
        for y in [1500, 3000, 4500, 6000, 8000]:
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(200)

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(800)

        scroll_status = await page.evaluate('''() => {
            const els = window.drones.getElements();
            return {
                total: els.length,
                built: els.filter(e => e.state === 'built').length,
                pending: els.filter(e => e.state === 'pending').length
            };
        }''')
        print(f"   Bottom status: {scroll_status}")
        assert scroll_status['pending'] == 0, f"Expected 0 pending elements at bottom, got {scroll_status['pending']}"

        # 6. Check Responsive Integrity across 6 Viewports
        print("\n6. Checking Responsive Layouts (0 Overflow)...")
        viewports = [
            (320, 568, "Mobile Small"),
            (375, 667, "Mobile Medium"),
            (768, 1024, "Tablet Portrait"),
            (1024, 768, "Tablet Landscape"),
            (1440, 900, "Desktop HD"),
            (2560, 1440, "Desktop 4K")
        ]
        for w, h, name in viewports:
            await page.set_viewport_size({'width': w, 'height': h})
            await page.wait_for_timeout(150)
            overflow = await page.evaluate('''() => {
                return document.documentElement.scrollWidth - window.innerWidth;
            }''')
            print(f"   {name} ({w}x{h}): horizontal overflow = {overflow}px")
            assert overflow <= 1, f"Horizontal overflow detected on {name}: {overflow}px"

        # 7. Check All Navigation & Anchor Links
        print("\n7. Checking Nav Links & External Social Links...")
        links_status = await page.evaluate('''() => {
            const navLinks = Array.from(document.querySelectorAll('.nav-links a, .hero-cta-group a, .dock-action-btn'));
            const socialLinks = Array.from(document.querySelectorAll('a[href^="http"]'));
            return {
                navLinksCount: navLinks.length,
                socialLinksCount: socialLinks.length,
                allSocialHaveBlank: socialLinks.every(a => a.getAttribute('target') === '_blank' || a.href.includes('mailto')),
                allSocialHaveNoopener: socialLinks.every(a => (a.getAttribute('rel') || '').includes('noopener') || a.href.includes('mailto'))
            };
        }''')
        print(f"   Nav links: {links_status['navLinksCount']}, Social links: {links_status['socialLinksCount']}")
        print(f"   Social links target=_blank: {links_status['allSocialHaveBlank']}")
        print(f"   Social links rel=noopener: {links_status['allSocialHaveNoopener']}")

        # 8. Check Final Console Errors
        print("\n8. Checking Console Errors...")
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print(f"   Total Console Errors: {len(actual_errors)}")
        if actual_errors:
            for err in actual_errors:
                print(f"     ! {err}")
        assert len(actual_errors) == 0, f"Expected 0 console errors, got {actual_errors}"

        # 9. Capture Full Final Showcase Screenshot
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.evaluate("document.getElementById('about-me').scrollIntoView()")
        await page.wait_for_timeout(400)
        final_ss = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/production_launch_about_code.png"
        await page.screenshot(path=final_ss)
        print(f"\n   Saved showcase screenshot: {final_ss}")

        print("\n=======================================================")
        print("🎉 PRE-LAUNCH PRODUCTION AUDIT PASSED 100% SUCCESSFULLY!")
        print("=======================================================")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
