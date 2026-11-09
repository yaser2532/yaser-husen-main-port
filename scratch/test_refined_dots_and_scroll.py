import sys
import time
from playwright.sync_api import sync_playwright

def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()

        page.on('console', lambda msg: print(f"[Browser Console {msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: errors.append(str(err)))

        # Abort heavy video/audio streaming in headless test to avoid socket stalls
        page.route("**/*.mp4", lambda route: route.abort())
        page.route("**/*.mp3", lambda route: route.abort())

        print("Navigating to http://localhost:8080/...")
        page.goto("http://localhost:8080/", wait_until='domcontentloaded')
        page.wait_for_timeout(1000)

        # 1. Verify Dots Sizing and Styling
        dots = page.query_selector_all('.mouse-tracker-dot')
        print(f"Found {len(dots)} dots.")
        assert len(dots) == 8, f"Expected 8 dots, found {len(dots)}"

        dot_metrics = page.evaluate("""() => {
            const dots = Array.from(document.querySelectorAll('.mouse-tracker-dot'));
            return dots.map((d, i) => {
                const comp = window.getComputedStyle(d);
                return {
                    index: i,
                    width: comp.width,
                    height: comp.height,
                    border: comp.border,
                    boxShadow: comp.boxShadow,
                    background: comp.background
                };
            });
        }""")

        for d in dot_metrics:
            print(f"Dot {d['index']}: width={d['width']}, height={d['height']}, border={d['border']}, boxShadow={d['boxShadow']}")
            # Size check: smaller radius (5px or 6px diameter)
            w_num = float(d['width'].replace('px', ''))
            assert w_num <= 7.0, f"Expected small dot radius (<= 7px diameter), got {w_num}px"
            # Bright white border check
            assert 'rgb(255, 255, 255)' in d['border'], f"Expected white border, got {d['border']}"
            # Bright white box shadow check
            assert 'rgb(255, 255, 255)' in d['boxShadow'], f"Expected white shadow, got {d['boxShadow']}"

        # 2. Test Text Hover Transparency
        print("Testing text hover transparency...")
        # Hover over hero title
        hero_title = page.query_selector('.hero-title') or page.query_selector('h1')
        assert hero_title is not None, "Hero title not found"
        title_box = hero_title.bounding_box()
        page.mouse.move(title_box['x'] + title_box['width'] / 2, title_box['y'] + title_box['height'] / 2)
        page.wait_for_timeout(350)

        is_cursor_reading = page.evaluate("() => document.body.classList.contains('cursor-reading')")
        title_hover_opacity = page.evaluate("""() => {
            const dot = document.querySelector('.mouse-tracker-dot');
            return parseFloat(window.getComputedStyle(dot).opacity);
        }""")
        print(f"When hovering over title: cursor-reading={is_cursor_reading}, dot opacity={title_hover_opacity}")
        assert is_cursor_reading is True, "Expected cursor-reading class on body when hovering over title"
        assert title_hover_opacity < 0.1, f"Expected transparent dots on text hover (opacity < 0.1), got {title_hover_opacity}"

        # Move mouse away to empty background area
        print("Testing return to active opacity when mouse leaves text...")
        page.mouse.move(50, 50)
        page.wait_for_timeout(400)
        bg_hover_opacity = page.evaluate("""() => {
            const dot = document.querySelector('.mouse-tracker-dot');
            return parseFloat(window.getComputedStyle(dot).opacity);
        }""")
        print(f"When hovering over blank background: dot opacity={bg_hover_opacity}")
        assert bg_hover_opacity > 0.6, f"Expected dots to become visible again, got {bg_hover_opacity}"

        # 3. Test Section Sequential Priority Sort Order
        print("Verifying pull-build sequential priority order (Title 1st, Paragraph 2nd, etc.)...")
        section_node_orders = page.evaluate("""() => {
            const sc = window.SectionCoordinator;
            if (!sc) return null;
            const res = {};
            ['about-me', 'projects', 'profile-expertise'].forEach(secId => {
                const nodes = sc.getNodesForSection(secId);
                res[secId] = nodes.map(n => ({
                    tag: n.el.tagName.toLowerCase(),
                    className: n.el.className,
                    order: n.order,
                    isText: n.isText
                }));
            });
            return res;
        }""")

        for secId, nodes in section_node_orders.items():
            print(f"Section [{secId}] nodes sequence:")
            for n in nodes[:5]:
                print(f"   Order {n['order']}: <{n['tag']}> class='{n['className'][:40]}'")
            # Verify first node is title
            first_node = nodes[0]
            assert first_node['tag'] in ['h1', 'h2', 'h3'] or 'section-title' in first_node['className'], \
                f"Expected first node in {secId} to be a Title/Heading, got {first_node['tag']}"
            # Verify second node is paragraph/intro
            if len(nodes) > 1:
                second_node = nodes[1]
                assert second_node['tag'] in ['h4', 'h5', 'h6', 'p'] or 'section-desc' in second_node['className'] or 'section-tag' in second_node['className'], \
                    f"Expected second node in {secId} to be a paragraph/subheading, got {second_node['tag']}"

        # 4. Test Smooth Scrolling & Capture Screenshots
        print("Testing smooth scroll across entire page...")
        for y in range(0, 3200, 200):
            page.mouse.wheel(0, 200)
            page.wait_for_timeout(50)

        page.wait_for_timeout(1000)

        # Capture screenshot of built section
        screenshot_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/refined_cyber_dots_preview.png"
        page.screenshot(path=screenshot_path)
        print(f"Refined screenshot saved to {screenshot_path}")

        browser.close()

    if errors:
        print(f"Errors encountered: {errors}")
        sys.exit(1)
    else:
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
