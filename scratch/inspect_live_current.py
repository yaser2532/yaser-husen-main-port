import os
from playwright.sync_api import sync_playwright

def inspect_live():
    print("--- INSPECTING CURRENT LIVE PORTFOLIO ON LOCALHOST:8080 ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()

        console_logs = []
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page_errors = []
        page.on('pageerror', lambda err: page_errors.append(str(err)))

        try:
            page.goto('http://localhost:8080/', wait_until='networkidle', timeout=10000)
        except Exception as e:
            print("Goto timeout or error, continuing...", e)

        page.wait_for_timeout(2000)

        # Print all console messages
        print("\n--- Console Output ---")
        for log in console_logs:
            print(log)

        print("\n--- Page Errors ---")
        for err in page_errors:
            print("ERROR:", err)

        # Artifact dir
        artifact_dir = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

        # Capture Hero Section
        hero_path = os.path.join(artifact_dir, "live_current_hero.png")
        page.screenshot(path=hero_path)
        print(f"Captured Hero screenshot: {hero_path}")

        # Scroll down to Expertise
        page.evaluate("() => window.scrollTo(0, 850)")
        page.wait_for_timeout(1500)
        exp_path = os.path.join(artifact_dir, "live_current_expertise.png")
        page.screenshot(path=exp_path)
        print(f"Captured Expertise screenshot: {exp_path}")

        # Scroll down to Projects
        page.evaluate("() => window.scrollTo(0, 2200)")
        page.wait_for_timeout(1500)
        proj_path = os.path.join(artifact_dir, "live_current_projects.png")
        page.screenshot(path=proj_path)
        print(f"Captured Projects screenshot: {proj_path}")

        # Scroll to Footer / Contact
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)
        footer_path = os.path.join(artifact_dir, "live_current_footer.png")
        page.screenshot(path=footer_path)
        print(f"Captured Footer screenshot: {footer_path}")

        # Full page screenshot
        full_path = os.path.join(artifact_dir, "live_current_fullpage.png")
        page.screenshot(path=full_path, full_page=True)
        print(f"Captured Full Page screenshot: {full_path}")

        # Check DOM status
        dom_status = page.evaluate("""() => {
            return {
                title: document.title,
                drones: document.querySelectorAll('.drone-unit, .mouse-tracker-dot').length,
                canvas: Array.from(document.querySelectorAll('canvas')).map(c => ({ id: c.id, width: c.width, height: c.height })),
                activeAudio: Boolean(document.getElementById('bgMusic')),
                sections: Array.from(document.querySelectorAll('section, header, footer')).map(s => ({
                    id: s.id,
                    dataNb: s.getAttribute('data-nb'),
                    visible: window.getComputedStyle(s).display !== 'none' && window.getComputedStyle(s).visibility !== 'hidden'
                }))
            };
        }""")
        print("\n--- DOM Inspection Status ---")
        print(dom_status)

        browser.close()

if __name__ == '__main__':
    inspect_live()
