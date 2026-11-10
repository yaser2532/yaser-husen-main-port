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

        # 1. Verify seam dimensions and position
        seam_info = await page.evaluate('''() => {
            const seam = document.querySelector('.hero-transition-seam');
            const home = document.getElementById('home');
            const prof = document.getElementById('profile-expertise');
            const sRect = seam.getBoundingClientRect();
            const hRect = home.getBoundingClientRect();
            const pRect = prof.getBoundingClientRect();
            const cs = window.getComputedStyle(seam);
            return {
                seamTop: sRect.top,
                seamBottom: sRect.bottom,
                seamHeight: sRect.height,
                homeBottom: hRect.bottom,
                profTop: pRect.top,
                backdropFilter: cs.backdropFilter || cs.webkitBackdropFilter,
                maskImage: cs.maskImage || cs.webkitMaskImage
            };
        }''')
        print("1. Seam Layout Info:", seam_info)
        # Seam must straddle across home bottom: top must be above homeBottom, bottom must be below homeBottom
        assert seam_info['seamTop'] < seam_info['homeBottom'], "Seam top must be above home bottom"
        assert seam_info['seamBottom'] > seam_info['homeBottom'], "Seam bottom must be below home bottom"
        assert 'blur' in seam_info['backdropFilter'], "Seam must have backdrop blur"

        # 2. Scroll to boundary (scroll = 450) and take screenshot
        await page.evaluate("window.scrollTo(0, 450)")
        await page.wait_for_timeout(400)

        screenshot_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/blurred_boundary_mid_scroll.png"
        await page.screenshot(path=screenshot_path)
        print(f"2. Saved screenshot: {screenshot_path}")

        # 3. Analyze pixel smoothness across boundary (y = 430 to 470)
        img = Image.open(screenshot_path)
        max_delta = 0
        prev_avg = None
        deltas = []

        for y in range(430, 470):
            colors = [img.getpixel((x, y))[:3] for x in [200, 400, 720, 1000, 1200]]
            avg_color = [sum(c[i] for c in colors)//len(colors) for i in range(3)]
            avg_brightness = sum(avg_color) / 3
            if prev_avg is not None:
                step_delta = abs(avg_brightness - prev_avg)
                deltas.append((y, step_delta, avg_color))
                if step_delta > max_delta:
                    max_delta = step_delta
            prev_avg = avg_brightness

        print(f"3. Maximum 1-pixel brightness delta across seam: {max_delta:.2f}")
        # In a smooth blend, no single pixel step should have a sharp jump > 8 brightness units
        assert max_delta < 8.0, f"Expected smooth blend (delta < 8.0), got {max_delta:.2f}"
        print("   Pixel gradient is smoothly continuous with NO sharp dividing line!")

        # 4. Check console errors
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print("4. Console errors:", actual_errors)
        assert len(actual_errors) == 0, f"Expected 0 console errors, got: {actual_errors}"

        print("=== ALL BLUR SEAM VERIFICATIONS PASSED! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
