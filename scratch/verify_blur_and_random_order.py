import asyncio
import sys
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

        # 1. Verify PRJ stamps removed
        prj_stamps = await page.evaluate('''() => {
            return {
                prjTextCount: Array.from(document.querySelectorAll('*')).filter(el => 
                    el.children.length === 0 && /\\/\\/\\s*PRJ-\\d+/i.test(el.textContent)
                ).length,
                cyberIndexClasses: document.querySelectorAll('.prj-cyber-index').length
            };
        }''')
        print("1. PRJ Stamps Check:", prj_stamps)
        assert prj_stamps['prjTextCount'] == 0, f"Expected 0 PRJ stamps, found {prj_stamps['prjTextCount']}"
        assert prj_stamps['cyberIndexClasses'] == 0, f"Expected 0 .prj-cyber-index, found {prj_stamps['cyberIndexClasses']}"

        # 2. Verify Hero-to-Profile GSAP/Lenis Blur Scrub Transition
        # Check initial state at scroll = 0
        initial_styles = await page.evaluate('''() => {
            const hero = document.querySelector('#home .header-content') || document.getElementById('home');
            const profile = document.getElementById('profile-expertise');
            return {
                heroFilter: hero.style.filter,
                heroOpacity: hero.style.opacity,
                profileFilter: profile.style.filter
            };
        }''')
        print("2a. Initial blur styles (scroll=0):", initial_styles)

        # Scroll down 350px (middle of transition zone)
        await page.evaluate("window.scrollTo(0, 350)")
        await page.wait_for_timeout(350) # allow lerp RAF loop to interpolate smoothly

        mid_styles = await page.evaluate('''() => {
            const hero = document.querySelector('#home .header-content') || document.getElementById('home');
            const profile = document.getElementById('profile-expertise');
            return {
                scrollY: window.scrollY,
                heroFilter: hero.style.filter,
                heroTransform: hero.style.transform,
                heroOpacity: hero.style.opacity,
                profileFilter: profile.style.filter,
                profileTransform: profile.style.transform,
                profileOpacity: profile.style.opacity
            };
        }''')
        print("2b. Mid-transition styles (scroll=350):", mid_styles)
        assert 'blur' in mid_styles['heroFilter'], "Hero should be blurring out during transition"
        assert 'blur' in mid_styles['profileFilter'], "Profile should have optical blur during transition"
        assert float(mid_styles['heroOpacity']) < 1.0, "Hero opacity should fade as user scrolls down"

        # Scroll to 900px (past transition zone)
        await page.evaluate("window.scrollTo(0, 900)")
        await page.wait_for_timeout(450) # allow lerp to complete

        settled_styles = await page.evaluate('''() => {
            const profile = document.getElementById('profile-expertise');
            return {
                scrollY: window.scrollY,
                profileFilter: profile.style.filter,
                profileTransform: profile.style.transform
            };
        }''')
        print("2c. Settled styles (scroll=900):", settled_styles)
        # Profile blur should be cleared at rest
        assert settled_styles['profileFilter'] == '', f"Profile filter should be cleared at rest, got: {settled_styles['profileFilter']}"

        # 3. Check drone system path archetypes and one-at-a-time pulling
        drone_spec = await page.evaluate('''() => {
            const d = window.drones;
            const els = d.getElements();
            const secInfo = {};
            els.forEach(e => {
                if (!secInfo[e.secId]) secInfo[e.secId] = 0;
                secInfo[e.secId]++;
            });
            return {
                totalElements: els.length,
                sections: Object.keys(secInfo),
                types: Array.from(new Set(els.map(e => e.type)))
            };
        }''')
        print("3. Drone Spec Check:", drone_spec)

        # 4. Check one-at-a-time pull concurrency guarantee
        max_concurrent_pulling = 0
        for target_y in [1200, 1800, 2600, 3400]:
            await page.evaluate(f"window.scrollTo(0, {target_y})")
            await page.wait_for_timeout(250)
            pulling_count = await page.evaluate('''() => {
                const els = window.drones.getElements();
                return els.filter(e => e.state === 'dispatched' || e.state === 'pulling').length;
            }''')
            if pulling_count > max_concurrent_pulling:
                max_concurrent_pulling = pulling_count

        print(f"4. Max concurrent pulling elements observed: {max_concurrent_pulling}")
        assert max_concurrent_pulling <= 1, f"Expected at most 1 active pulling element at a time, got {max_concurrent_pulling}"

        # 5. Take screenshot of transition seam and profile expertise
        await page.evaluate("window.scrollTo(0, 400)")
        await page.wait_for_timeout(350)
        screenshot_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/test_gsap_blur_transition.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"5. Saved screenshot to {screenshot_path}")

        # Filter harmless favicon or font warnings if any
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print("Console errors:", actual_errors)
        assert len(actual_errors) == 0, f"Expected 0 console errors, got: {actual_errors}"

        print("=== ALL CHECKS PASSED SUCCESSFULLY! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
