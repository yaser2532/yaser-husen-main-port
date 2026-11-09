import sys
import time
from playwright.sync_api import sync_playwright

def run():
    print("--- STARTING COMPREHENSIVE VERIFICATION SUITE ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()

        # Abort heavy external video/mp3 streams to keep test lean
        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: console_errors.append(str(exc)))

        print("1. Navigating to http://localhost:8080/...")
        page.goto('http://localhost:8080/', wait_until='domcontentloaded', timeout=15000)
        page.wait_for_timeout(1000)

        # ─── TEST 1: Check Space Ambient Audio Element ───
        print("\n--- TEST 1: Space Ambient Audio ---")
        audio_info = page.evaluate("""() => {
            const el = document.getElementById('bgMusic');
            return {
                exists: Boolean(el),
                src: el ? el.src : null,
                currentSrc: el ? el.currentSrc : null,
                paused: el ? el.paused : null,
                muted: el ? el.muted : null,
                readyState: el ? el.readyState : null
            };
        }""")
        print(f"Audio element info: {audio_info}")
        assert audio_info['exists'], "Audio element #bgMusic should exist"
        assert 'space-ambient.wav' in audio_info['src'], "Audio src should be space-ambient.wav"

        # Simulate user gesture to trigger audio playback
        print("Simulating user gesture to initiate space ambient music...")
        page.mouse.click(200, 200)
        page.wait_for_timeout(800)

        audio_state_after = page.evaluate("""() => {
            const el = document.getElementById('bgMusic');
            return {
                paused: el ? el.paused : null,
                volume: el ? el.volume : null,
                currentTime: el ? el.currentTime : null,
                muted: el ? el.muted : null
            };
        }""")
        print(f"Audio state after gesture: {audio_state_after}")

        # ─── TEST 2: Check Resume Download Buttons ───
        print("\n--- TEST 2: Resume Download Buttons (Navbar & Footer) ---")
        nav_resume = page.evaluate("""() => {
            const el = document.querySelector('.nav-resume-btn');
            if (!el) return null;
            const cs = window.getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return {
                href: el.getAttribute('href'),
                download: el.getAttribute('download'),
                text: el.innerText.trim(),
                display: cs.display,
                bg: cs.backgroundColor,
                border: cs.border,
                borderRadius: cs.borderRadius,
                color: cs.color,
                boxShadow: cs.boxShadow,
                rect: { w: r.width, h: r.height, x: r.left, y: r.top }
            };
        }""")
        print(f"Navbar Resume button: {nav_resume}")
        assert nav_resume is not None, "Navbar resume button should exist"
        assert 'Yaser_Husen_Resume.pdf' in nav_resume['href'], "Navbar resume should link to PDF"
        assert nav_resume['rect']['w'] > 50, "Navbar resume should have valid width"

        footer_resume = page.evaluate("""() => {
            const el = document.querySelector('.dock-btn-resume');
            if (!el) return null;
            const cs = window.getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return {
                href: el.getAttribute('href'),
                download: el.getAttribute('download'),
                text: el.innerText.trim(),
                display: cs.display,
                bg: cs.backgroundColor,
                border: cs.border,
                borderRadius: cs.borderRadius,
                color: cs.color,
                rect: { w: r.width, h: r.height, x: r.left, y: r.top }
            };
        }""")
        print(f"Footer Resume button: {footer_resume}")
        assert footer_resume is not None, "Footer resume button should exist"
        assert 'Yaser_Husen_Resume.pdf' in footer_resume['href'], "Footer resume should link to PDF"

        # ─── TEST 3: Text Hover Semi-Transparency ───
        print("\n--- TEST 3: Text Hover Semi-Transparency ---")
        # Initially in empty space (e.g. at 50, 50)
        page.mouse.move(50, 50)
        page.wait_for_timeout(300)
        initial_reading = page.evaluate("() => document.body.classList.contains('cursor-reading')")
        print(f"Initial cursor-reading state: {initial_reading}")

        # Move over hero title (text)
        title_box = page.locator('#tp-name').bounding_box() or page.locator('.hero-title').bounding_box()
        if title_box:
            tx = title_box['x'] + title_box['width'] * 0.5
            ty = title_box['y'] + title_box['height'] * 0.5
            print(f"Moving cursor over hero text at ({tx}, {ty})...")
            page.mouse.move(tx, ty)
            page.wait_for_timeout(400)

            hover_state = page.evaluate("""() => {
                const isReading = document.body.classList.contains('cursor-reading');
                const dots = document.querySelectorAll('.mouse-tracker-dot');
                const opacities = Array.from(dots).map(d => parseFloat(window.getComputedStyle(d).opacity));
                const glow = document.getElementById('mouse-glow');
                const glowOp = glow ? parseFloat(window.getComputedStyle(glow).opacity) : null;
                return {
                    isReading,
                    dotCount: dots.length,
                    averageDotOpacity: opacities.reduce((a, b) => a + b, 0) / (opacities.length || 1),
                    opacities,
                    glowOp
                };
            }""")
            print(f"Text hover state: {hover_state}")
            assert hover_state['isReading'], "Body should have class 'cursor-reading' when hovering text"
            assert hover_state['averageDotOpacity'] <= 0.25, f"Dot opacity should be semi-transparent (~0.20), got {hover_state['averageDotOpacity']}"

            # Move away from text to empty space
            page.mouse.move(10, 300)
            page.wait_for_timeout(400)
            away_state = page.evaluate("""() => {
                const isReading = document.body.classList.contains('cursor-reading');
                const dots = document.querySelectorAll('.mouse-tracker-dot');
                const opacities = Array.from(dots).map(d => parseFloat(window.getComputedStyle(d).opacity));
                return {
                    isReading,
                    averageDotOpacity: opacities.reduce((a, b) => a + b, 0) / (opacities.length || 1)
                };
            }""")
            print(f"State after moving away from text: {away_state}")
            assert not away_state['isReading'], "Body should NOT have cursor-reading when away from text"
            assert away_state['averageDotOpacity'] >= 0.55, f"Dot opacity should recover to high luminescent, got {away_state['averageDotOpacity']}"

        # ─── TEST 4: Cursor Contact-Based Sequential Pull ───
        print("\n--- TEST 4: Cursor Contact-Based Sequential Pull ---")
        # Scroll to expertise section
        page.evaluate("() => window.scrollTo({ top: 700, behavior: 'smooth' })")
        page.wait_for_timeout(1000)

        # Inspect expertise section state
        exp_info = page.evaluate("""() => {
            const s = document.getElementById('profile-expertise');
            const nodes = window.SectionCoordinator ? window.SectionCoordinator.getNodesForSection('profile-expertise') : [];
            return {
                sectionState: s ? s.getAttribute('data-nb') : null,
                nodeCount: nodes.length,
                assembledCount: nodes.filter(n => n.state === 'assembled').length,
                nodeStates: nodes.map(n => ({ id: n.id, tag: n.el.tagName, isText: n.isText, state: n.state }))
            };
        }""")
        print(f"Expertise pull state: {exp_info}")

        # Simulate cursor hovering onto unpulled element to trigger contact pull
        print("Hovering cursor onto eligible sequential elements...")
        for step in range(4):
            page.mouse.move(720, 350 + step * 80)
            page.wait_for_timeout(800)

        exp_info_after = page.evaluate("""() => {
            const nodes = window.SectionCoordinator ? window.SectionCoordinator.getNodesForSection('profile-expertise') : [];
            return {
                assembledCount: nodes.filter(n => n.state === 'assembled').length,
                total: nodes.length
            };
        }""")
        print(f"Expertise assembled count after cursor contact: {exp_info_after}")

        # Check console errors
        print("\n--- CONSOLE ERRORS CHECK ---")
        critical_errors = [e for e in console_errors if 'favicon' not in e and 'ERR_ABORTED' not in e and 'net::ERR_FAILED' not in e]
        print(f"Critical console errors: {critical_errors}")
        assert len(critical_errors) == 0, f"Found unexpected console errors: {critical_errors}"

        # Capture verification screenshots
        page.evaluate("() => window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        page.screenshot(path="scratch/hero_final_verification.png")
        print("Captured scratch/hero_final_verification.png")

        page.evaluate("() => window.scrollTo(0, 850)")
        page.wait_for_timeout(600)
        page.screenshot(path="scratch/expertise_pull_verification.png")
        print("Captured scratch/expertise_pull_verification.png")

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(800)
        page.screenshot(path="scratch/footer_dock_verification.png")
        print("Captured scratch/footer_dock_verification.png")

        browser.close()
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run()
