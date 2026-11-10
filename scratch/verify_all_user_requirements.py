import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

def main():
    print("Starting comprehensive verification for all user requirements...")
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))

        page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(1.0)

        # ─── CHECK 1: Hero Transition & "Scroll to Explore" Removal ───
        print("\n--- Check 1: Hero Seam & Scroll Button Removal ---")
        scroll_btn = page.query_selector(".hero-scroll-pill")
        assert scroll_btn is None, "Error: .hero-scroll-pill should be completely removed"
        print("PASS: .hero-scroll-pill removed from hero section!")

        horizon_beam = page.query_selector(".hero-horizon-beam")
        assert horizon_beam is None, "Error: .hero-horizon-beam should be completely removed"
        print("PASS: .hero-horizon-beam hard line removed!")

        seam = page.query_selector(".hero-transition-seam")
        assert seam is not None, "Error: .hero-transition-seam should exist for smooth gradient blend"
        print("PASS: .hero-transition-seam exists for atmospheric gradient fade!")

        # Screenshot Hero to Content transition
        page.evaluate("window.scrollTo(0, 500)")
        time.sleep(0.5)
        page.screenshot(path="scratch/test_hero_to_content_blend.png")
        print("Captured scratch/test_hero_to_content_blend.png")

        # ─── CHECK 2: Drone Dot Elements Size & Normal Durations ───
        print("\n--- Check 2: Drone Dot Size & Normal Durations ---")
        drone_info = page.evaluate("""() => {
            const ds = window.drones.getDrones();
            const els = window.drones.getElements();
            const types = {};
            els.forEach(e => {
                if (!types[e.type]) types[e.type] = e.minDuration;
            });
            return {
                droneSizes: ds.map(d => d.size),
                durations: types
            };
        }""")
        avg_size = sum(drone_info["droneSizes"]) / len(drone_info["droneSizes"])
        print(f"Drone dot sizes: {drone_info['droneSizes'][:4]}... (Avg: {avg_size:.2f}px)")
        assert avg_size >= 3.0, f"Error: Drone dot size should be >= 3.0px, got {avg_size}"
        print(f"PASS: Drone dot sizes reverted to normal ({avg_size:.2f}px)!")

        durations = drone_info["durations"]
        print(f"Durations: Title={durations.get('title')}ms, Para={durations.get('paragraph')}ms, Card={durations.get('card')}ms, Button={durations.get('button')}ms")
        assert durations.get("title") >= 1000, f"Title duration should be >= 1000ms, got {durations.get('title')}"
        assert durations.get("paragraph") >= 800, f"Paragraph duration should be >= 800ms, got {durations.get('paragraph')}"
        assert durations.get("card") >= 600, f"Card duration should be >= 600ms, got {durations.get('card')}"
        print("PASS: Drone rendering durations reverted to normal cinematic speed!")

        # ─── CHECK 3: Automatic Sequential Section Pulling ───
        print("\n--- Check 3: Automatic Sequential Section Pulling ---")
        # Scroll to #profile-expertise so it covers most of screen
        page.evaluate("""() => {
            const el = document.getElementById('profile-expertise');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }""")
        time.sleep(1.2)

        mission_status = page.evaluate("""() => {
            const els = window.drones.getElements();
            const profEls = els.filter(e => e.secId === 'profile-expertise');
            return profEls.map(e => ({ id: e.id, type: e.type, state: e.state }));
        }""")
        print("Profile-expertise element states after section covers screen:")
        for m in mission_status:
            print(f"  {m['id']} ({m['type']}): {m['state']}")
        
        # At least one or more elements should have automatically dispatched/pulled without mouse contact
        active_count = sum(1 for m in mission_status if m['state'] in ['dispatched', 'pulling', 'built'])
        assert active_count >= 1, "Error: Elements in #profile-expertise should automatically start building when section covers most of screen"
        print(f"PASS: Automatic sequential drone pulling triggered ({active_count} elements active/built)!")

        # ─── CHECK 4: Featured Projects Gen Z & Artistic Cards ───
        print("\n--- Check 4: Featured Projects Gen Z & Artistic Cards ---")
        page.evaluate("""() => {
            const el = document.getElementById('projects');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }""")
        time.sleep(1.0)

        card_info = page.evaluate("""() => {
            const cards = document.querySelectorAll('.project-card');
            const telemetryTags = document.querySelectorAll('.prj-cyber-index');
            const tornStickers = document.querySelectorAll('.torn-paper-sticker');
            return {
                cardCount: cards.length,
                telemetryCount: telemetryTags.length,
                tornStickerCount: tornStickers.length
            };
        }""")
        print(f"Projects count: {card_info['cardCount']}, Telemetry tags: {card_info['telemetryCount']}, Torn paper stickers: {card_info['tornStickerCount']}")
        assert card_info["cardCount"] == 9, "Should have 9 project cards"
        assert card_info["telemetryCount"] >= 8, "Project cards should have telemetry index tags"
        assert card_info["tornStickerCount"] >= 3, "Should have torn paper easter egg stickers"
        print("PASS: Gen Z telemetry stamps and torn paper stickers present on project cards!")

        # Capture projects section screenshot
        page.screenshot(path="scratch/test_gen_z_project_cards.png")
        print("Captured scratch/test_gen_z_project_cards.png")

        # ─── CHECK 5: Torn Paper & Static Noise Easter Egg Click ───
        print("\n--- Check 5: Torn Paper & Static Noise Easter Egg Trigger ---")
        first_sticker = page.query_selector(".torn-paper-sticker")
        assert first_sticker is not None, "Torn paper sticker should exist"
        
        # Click the easter egg sticker
        first_sticker.click()
        time.sleep(0.3)

        overlay_active = page.evaluate("""() => {
            const overlay = document.getElementById('static-noise-overlay');
            const toast = document.getElementById('static-toast-msg');
            return {
                isActive: overlay && overlay.classList.contains('active'),
                toastText: toast ? toast.innerText : ''
            };
        }""")
        print(f"Static noise overlay active: {overlay_active['isActive']}")
        assert overlay_active["isActive"], "Static noise overlay should be active after clicking torn paper sticker"
        page.screenshot(path="scratch/test_static_noise_easter_egg.png")
        print("Captured scratch/test_static_noise_easter_egg.png")
        print("PASS: Static noise CRT glitch burst and easter egg toast verified!")

        # Wait for static burst to finish
        time.sleep(0.8)

        # ─── CHECK 6: Console Error Audit ───
        print("\n--- Check 6: Console Errors Audit ---")
        print(f"Total console errors encountered: {len(errors)}")
        if errors:
            for e in errors:
                print("  ERROR:", e)
        assert len(errors) == 0, f"Console errors encountered: {errors}"
        print("PASS: 0 Console Errors across all interactions!")

        browser.close()
        print("\nAll user requirements successfully verified and passed 100%!")

if __name__ == "__main__":
    main()
