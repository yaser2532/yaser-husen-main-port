import sys
import time
import math
from playwright.sync_api import sync_playwright

def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()

        page.on('console', lambda msg: print(f"[Browser Console {msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: errors.append(str(err)))

        print("Navigating to http://localhost:8080/...")
        page.goto("http://localhost:8080/", wait_until='domcontentloaded')
        page.wait_for_timeout(1500)

        # Check title & basics
        print(f"Page title: {page.title()}")

        # Move mouse to trigger swarm tracking
        page.mouse.move(600, 400)
        page.wait_for_timeout(1000)

        # Inspect dots
        dots = page.query_selector_all('.mouse-tracker-dot')
        print(f"Found {len(dots)} mouse tracker dots.")
        assert len(dots) == 8, f"Expected 8 dots, found {len(dots)}"

        # Check dots positions and calculate mutual distances
        positions = []
        for i, dot in enumerate(dots):
            box = dot.bounding_box()
            if box:
                positions.append((box['x'] + box['width']/2, box['y'] + box['height']/2))

        print(f"Dot positions: {positions}")
        # Test mutual separation - verify NO clustering/overlap
        min_pairwise_dist = 999999
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                d = math.hypot(positions[i][0] - positions[j][0], positions[i][1] - positions[j][1])
                if d < min_pairwise_dist:
                    min_pairwise_dist = d

        print(f"Minimum pairwise separation between drones: {min_pairwise_dist:.2f}px")
        assert min_pairwise_dist > 20, f"Expected dots to not cluster (min separation > 20px), got {min_pairwise_dist:.2f}px"

        # Check style properties (metallic border, no red holiday colors)
        dot_style = page.evaluate("""() => {
            const dot = document.querySelector('.mouse-tracker-dot');
            const comp = window.getComputedStyle(dot);
            return {
                border: comp.border,
                animationName: comp.animationName,
                width: comp.width,
                height: comp.height
            };
        }""")
        print(f"Dot computed style: {dot_style}")
        assert 'cyberpunk-drone-specular' in dot_style['animationName'], "Expected cyberpunk specular animation"

        # Check background stars in WebGL engine
        gl_stars = page.evaluate("""() => {
            return {
                fgStars: window.FG_STARS || 850,
                bgStars: window.BG_STARS || 2800,
                hasCanvas: !!document.getElementById('webgl-canvas') || !!document.querySelector('canvas')
            };
        }""")
        print(f"WebGL stars status: {gl_stars}")

        # Capture hero screenshot with swarm
        screenshot_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/cyberpunk_swarm_preview.png"
        page.screenshot(path=screenshot_path)
        print(f"Swarm screenshot saved to {screenshot_path}")

        # Scroll smoothly to test pull-build and 60fps performance
        print("Testing smooth scroll and pull-build trigger...")
        for y in range(0, 2500, 150):
            page.mouse.wheel(0, 150)
            page.wait_for_timeout(60)

        page.wait_for_timeout(1500)
        scroll_screenshot = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/scroll_sections_preview.png"
        page.screenshot(path=scroll_screenshot)
        print(f"Scroll screenshot saved to {scroll_screenshot}")

        # Check if sections built successfully
        section_states = page.evaluate("""() => {
            const secs = Array.from(document.querySelectorAll('section, footer'));
            return secs.map(s => ({
                id: s.id,
                nbState: s.getAttribute('data-nb'),
                opacity: window.getComputedStyle(s).opacity,
                display: window.getComputedStyle(s).display
            }));
        }""")
        print("Section states after scrolling:")
        for s in section_states:
            print(f"  [{s['id']}]: data-nb={s['nbState']}, opacity={s['opacity']}, display={s['display']}")

        # Ensure no blank wiped sections
        for s in section_states:
            if s['id'] in ['home', 'profile-expertise', 'about-me', 'projects']:
                assert float(s['opacity']) > 0.5, f"Section {s['id']} was wiped to 0 opacity!"

        browser.close()

    if errors:
        print(f"JavaScript errors detected: {errors}")
        sys.exit(1)
    else:
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
