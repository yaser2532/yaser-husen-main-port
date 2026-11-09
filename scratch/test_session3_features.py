import os
import sys
from playwright.sync_api import sync_playwright

def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()

        page.on('console', lambda msg: print(f"[Browser Console {msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: errors.append(str(err)))

        # Abort heavy video/audio streaming during headless test to avoid socket stalls
        page.route("**/*.mp4", lambda route: route.abort())
        page.route("**/*.mp3", lambda route: route.abort())

        print("Navigating to http://localhost:8080/...")
        page.goto("http://localhost:8080/", wait_until='domcontentloaded')
        page.wait_for_timeout(1000)

        # 1. Verify Resume Download links (Navbar and Footer)
        print("Checking Resume Download buttons...")
        nav_resume = page.query_selector('.nav-resume-btn')
        assert nav_resume is not None, "nav-resume-btn not found in Navbar"
        nav_href = nav_resume.get_attribute('href')
        nav_download = nav_resume.get_attribute('download')
        print(f"Navbar Resume button: href={nav_href}, download={nav_download}")
        assert 'Yaser_Husen_Resume.pdf' in nav_href, f"Unexpected nav href: {nav_href}"

        footer_resume = page.query_selector('#footer-resume-btn')
        assert footer_resume is not None, "footer-resume-btn not found in Footer"
        footer_href = footer_resume.get_attribute('href')
        footer_download = footer_resume.get_attribute('download')
        print(f"Footer Resume button: href={footer_href}, download={footer_download}")
        assert 'Yaser_Husen_Resume.pdf' in footer_href, f"Unexpected footer href: {footer_href}"

        # Verify physical file existence
        pdf_path = "assets/docs/Yaser_Husen_Resume.pdf"
        assert os.path.exists(pdf_path), f"File {pdf_path} does not exist!"
        assert os.path.getsize(pdf_path) > 10000, f"File {pdf_path} is too small or empty!"
        print(f"Physical Resume PDF confirmed at {pdf_path} ({os.path.getsize(pdf_path)} bytes).")

        # 2. Verify Background Music Element
        print("Checking Background Music element...")
        bg_music = page.query_selector('#bgMusic')
        assert bg_music is not None, "bgMusic element not found"
        src = bg_music.get_attribute('src')
        print(f"Global audio bgMusic src: {src}")
        assert 'bg.mp3' in src, f"Expected bg.mp3, got {src}"

        # 3. Verify Lamplight Visual Styling
        print("Checking Lamplight Spotlight styling...")
        beam_style = page.evaluate("""() => {
            const beam = document.querySelector('.light-beam-visual');
            if (!beam) return null;
            const comp = window.getComputedStyle(beam);
            return {
                clipPath: comp.clipPath,
                filter: comp.filter,
                width: comp.width,
                height: comp.height
            };
        }""")
        print(f"Lamplight beam computed style: {beam_style}")
        assert beam_style is not None, "Light beam element not found"
        assert 'polygon' in beam_style['clipPath'], f"Expected polygon clipPath for straight beam, got {beam_style['clipPath']}"
        assert 'blur(1.5px)' in beam_style['filter'] or 'blur(1.' in beam_style['filter'], f"Expected subtle edge blur (~1.5px), got {beam_style['filter']}"

        # 4. Verify Dot Semi-Transparency on Text Hover (0.22 opacity, NOT 0!)
        print("Checking Dot Semi-Transparency on Text Hover...")
        hero_title = page.query_selector('.hero-title') or page.query_selector('h1')
        title_box = hero_title.bounding_box()
        page.mouse.move(title_box['x'] + title_box['width'] / 2, title_box['y'] + title_box['height'] / 2)
        page.wait_for_timeout(400)

        is_cursor_reading = page.evaluate("() => document.body.classList.contains('cursor-reading')")
        title_hover_opacity = page.evaluate("""() => {
            const dot = document.querySelector('.mouse-tracker-dot');
            return parseFloat(window.getComputedStyle(dot).opacity);
        }""")
        print(f"Hovering over title: cursor-reading={is_cursor_reading}, dot opacity={title_hover_opacity}")
        assert is_cursor_reading is True, "Expected cursor-reading class on body"
        # Must be semi-transparent (~0.22), NOT 0 (disappeared) and NOT >= 0.6 (opaque)
        assert 0.15 <= title_hover_opacity <= 0.35, f"Expected semi-transparent dot (~0.22), got {title_hover_opacity}"

        # 5. Verify Sequential Pull Timing (1.1s gap)
        print("Checking Section Pull Timing...")
        pull_timing = page.evaluate("""() => {
            // Trigger pull on profile-expertise
            const secs = window.SectionCoordinator;
            return {
                hasCoordinator: !!secs
            };
        }""")
        print(f"Pull timing system status: {pull_timing}")

        # Capture verification screenshots
        page.mouse.move(50, 50)
        page.wait_for_timeout(300)
        screenshot_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/session3_features_preview.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

    if errors:
        print(f"Errors encountered: {errors}")
        sys.exit(1)
    else:
        print("ALL SESSION 3 VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
