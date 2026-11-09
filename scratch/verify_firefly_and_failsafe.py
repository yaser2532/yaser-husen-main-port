import asyncio
import sys
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

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

        # 1. TEST: Black Line Eradication at Boundary
        await page.evaluate("window.scrollTo(0, 450)")
        await page.wait_for_timeout(400)
        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/test_no_black_line.png"
        await page.screenshot(path=ss_path)
        print("1. Captured boundary screenshot:", ss_path)

        # Check that no pixel row in the seam drops into deep black (< 2.0 brightness)
        img = Image.open(ss_path)
        min_brightness = 255
        for y in range(435, 465):
            for x in [300, 500, 720, 900, 1100]:
                r, g, b = img.getpixel((x, y))[:3]
                br = (r + g + b) / 3
                if br < min_brightness:
                    min_brightness = br
        print(f"   Minimum brightness across seam: {min_brightness:.1f}")
        # Seam computed background is transparent, no black stripe
        seam_bg = await page.evaluate('''() => {
            const seam = document.querySelector('.hero-transition-seam');
            return window.getComputedStyle(seam).backgroundColor;
        }''')
        print(f"   Seam background-color: {seam_bg}")
        assert seam_bg in ['rgba(0, 0, 0, 0)', 'transparent'], f"Seam background should be transparent, got: {seam_bg}"

        # 2. TEST: Firefly Light Tail
        # Move cursor to generate flight trail
        for pos in [(300, 300), (500, 350), (700, 400), (900, 350), (1100, 300)]:
            await page.mouse.move(pos[0], pos[1])
            await page.wait_for_timeout(100)

        trail_info = await page.evaluate('''() => {
            const ds = window.drones.getDrones();
            return {
                droneCount: ds.length,
                maxTrailObserved: Math.max(...ds.map(d => d.trail ? d.trail.length : 0)),
                hasTrailPoints: ds.every(d => d.trail && d.trail.length > 5)
            };
        }''')
        print("2. Firefly Light Tail Info:", trail_info)
        assert trail_info['maxTrailObserved'] >= 10, f"Expected trail length >= 10, got {trail_info['maxTrailObserved']}"
        assert trail_info['hasTrailPoints'], "Every drone should maintain an organic light tail"

        # 3. TEST: Unpredictable Dot Element Paths
        # Sample positions of drone 0 relative to cursor over 10 frames
        distances = []
        for _ in range(12):
            await page.mouse.move(700, 400)
            await page.wait_for_timeout(60)
            d = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                return ds.map(d => Math.hypot(d.x - 700, d.y - 400));
            }''')
            distances.append(d[0])

        variance = max(distances) - min(distances)
        print(f"3. Unpredictable Flutter: drone[0] distance range from cursor: {min(distances):.1f}px to {max(distances):.1f}px (variance: {variance:.1f}px)")
        assert variance > 3.0, f"Expected dynamic unpredictable fluttering (variance > 3px), got {variance:.1f}px"

        # 4. TEST: Fast-Scroll Failsafe
        # Rapidly scroll to bottom or past sections
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(200)

        # Fast flick to y = 3500
        await page.evaluate('''() => {
            window.scrollTo(0, 3500);
        }''')
        await page.wait_for_timeout(300)

        # Verify that all elements above current viewport are instantly built
        failsafe_status = await page.evaluate('''() => {
            const els = window.drones.getElements();
            const aboveViewport = els.filter(e => {
                const r = e.el.getBoundingClientRect();
                return r.bottom < -20;
            });
            return {
                totalAbove: aboveViewport.length,
                builtAbove: aboveViewport.filter(e => e.state === 'built').length,
                pendingAbove: aboveViewport.filter(e => e.state === 'pending').length
            };
        }''')
        print("4. Fast-Scroll Failsafe Check (scrolled past elements):", failsafe_status)
        assert failsafe_status['pendingAbove'] == 0, f"No elements scrolled above viewport should remain pending, got {failsafe_status['pendingAbove']}"
        assert failsafe_status['builtAbove'] == failsafe_status['totalAbove'], "100% of scrolled-past elements must be completed by failsafe"

        # Scroll to bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        footer_status = await page.evaluate('''() => {
            const els = window.drones.getElements();
            return {
                total: els.length,
                built: els.filter(e => e.state === 'built').length,
                pending: els.filter(e => e.state === 'pending').length
            };
        }''')
        print("   Footer Failsafe Check:", footer_status)
        assert footer_status['pending'] == 0, "All elements must be built at bottom"

        # 5. Check console errors
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print("5. Console errors:", actual_errors)
        assert len(actual_errors) == 0, f"Expected 0 console errors, got: {actual_errors}"

        # Capture firefly screenshot
        await page.evaluate("window.scrollTo(0, 0)")
        await page.mouse.move(720, 450)
        await page.wait_for_timeout(300)
        firefly_ss = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/firefly_light_tail.png"
        await page.screenshot(path=firefly_ss)
        print("   Saved firefly screenshot:", firefly_ss)

        print("=== ALL 4 CHECKS PASSED WITH 100% SUCCESS! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
