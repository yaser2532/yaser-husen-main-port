from playwright.sync_api import sync_playwright

def test_upgrades():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())

        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        console_logs = []
        page.on('console', lambda m: console_logs.append(f"[{m.type}] {m.text}"))

        print("Navigating to http://localhost:8080/...")
        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(1500)

        # 1. Check Hero & Starfield
        hero_screen = "scratch/test_hero_upgraded.png"
        page.screenshot(path=hero_screen)
        print(f"Captured {hero_screen}")

        # 2. Scroll to Expertise (1000px)
        page.evaluate("() => window.scrollTo(0, 1000)")
        page.wait_for_timeout(1200)
        exp_screen = "scratch/test_expertise_upgraded.png"
        page.screenshot(path=exp_screen)
        print(f"Captured {exp_screen}")

        # 3. Hover over text to verify semi-transparency
        page.mouse.move(720, 400)
        page.wait_for_timeout(500)
        hover_data = page.evaluate("""() => {
            const isReading = document.body.classList.contains('cursor-reading');
            const dots = document.querySelectorAll('.mouse-tracker-dot');
            const opacities = Array.from(dots).map(d => parseFloat(window.getComputedStyle(d).opacity));
            return {
                isReading,
                count: dots.length,
                avgOpacity: opacities.reduce((a, b) => a + b, 0) / (opacities.length || 1),
                opacities
            };
        }""")
        print("Hover test data:", hover_data)

        # 4. Scroll to Projects (2500px)
        page.evaluate("() => window.scrollTo(0, 2500)")
        page.wait_for_timeout(1200)
        proj_screen = "scratch/test_projects_upgraded.png"
        page.screenshot(path=proj_screen)
        print(f"Captured {proj_screen}")

        # 5. Scroll to Footer
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1200)
        footer_screen = "scratch/test_footer_upgraded.png"
        page.screenshot(path=footer_screen)
        print(f"Captured {footer_screen}")

        # 6. Check console errors
        critical = [e for e in errors if 'favicon' not in e]
        print("Critical page errors:", critical)
        print("Console errors count:", len([l for l in console_logs if '[error]' in l]))
        for l in console_logs:
            if '[error]' in l and 'net::ERR_FAILED' not in l:
                print("Console Error:", l)

        browser.close()

if __name__ == '__main__':
    test_upgrades()
