from playwright.sync_api import sync_playwright

def test():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto('http://localhost:8080/')
        page.wait_for_timeout(1000)
        
        # 1. Check Multipurpose Firefly Drones / Dots
        dots_count = page.evaluate("() => window.swarm ? window.swarm.getDots().length : 0")
        print(f"Firefly dots / drones count: {dots_count}")
        assert dots_count == 8, f"Expected 8 multipurpose firefly dots, got {dots_count}"

        gl_drones_count = page.evaluate("() => window.__gl && window.__gl.drones ? window.__gl.drones.length : 0")
        print(f"window.__gl.drones count: {gl_drones_count}")
        assert gl_drones_count == 8, f"Expected 8 drones via __gl, got {gl_drones_count}"

        # 2. Check Starry Sky Canvas & Container
        cosmic_opacity = page.evaluate("() => { const c = document.getElementById('cosmic-bg-container'); return c ? window.getComputedStyle(c).opacity : 'missing'; }")
        print(f"Cosmic bg container opacity: {cosmic_opacity}")
        assert float(cosmic_opacity) >= 0.8, f"Expected cosmic background to be active with opacity >= 0.8, got {cosmic_opacity}"

        # 3. Check Hero Section 3D Interactive Name
        page.wait_for_timeout(1400) # Wait for typing to complete
        char_count = page.evaluate("() => document.querySelectorAll('#tp-name .hero-3d-char').length")
        print(f"Hero 3D characters count: {char_count}")
        assert char_count == 10, f"Expected 10 characters in 'YASER HUSEN', got {char_count}"

        # Test hover repulsion physics on first character ('Y')
        char_box = page.evaluate('''() => {
            const firstChar = document.querySelector('#tp-name .hero-3d-char');
            const r = firstChar.getBoundingClientRect();
            return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
        }''')
        
        # Move mouse near character
        page.mouse.move(char_box['x'] + 15, char_box['y'] + 10)
        page.wait_for_timeout(200)
        is_repelled = page.evaluate("() => document.querySelector('#tp-name .hero-3d-char').classList.contains('is-repelled')")
        print(f"Character 'Y' repelled when cursor nearby: {is_repelled}")
        assert is_repelled, "Character should have .is-repelled class when cursor is near"

        # Move mouse far away
        page.mouse.move(10, 10)
        page.wait_for_timeout(300)
        is_repelled_away = page.evaluate("() => document.querySelector('#tp-name .hero-3d-char').classList.contains('is-repelled')")
        print(f"Character 'Y' returns when cursor away: {not is_repelled_away}")
        assert not is_repelled_away, "Character should return to normal when cursor leaves"

        # 4. Check 4 Project Filter Buttons
        filter_texts = page.evaluate("() => Array.from(document.querySelectorAll('.project-filters .filter-btn')).map(b => b.innerText.trim())")
        print(f"Filter buttons: {filter_texts}")
        assert len(filter_texts) == 4, f"Expected 4 filter buttons, got {len(filter_texts)}"
        assert "All Projects" in filter_texts[0]
        assert "AI & Data Science Projects" in filter_texts[1]
        assert "Web Apps" in filter_texts[2]
        assert "Creative Labs" in filter_texts[3]

        # Check button styles are uniform
        filter_radii = page.evaluate("() => Array.from(document.querySelectorAll('.project-filters .filter-btn')).map(b => window.getComputedStyle(b).borderRadius)")
        print(f"Filter buttons border radii: {filter_radii}")
        assert len(set(filter_radii)) == 1, f"Expected all filter buttons to share identical border-radius, got {filter_radii}"

        # 5. Check Fast Section Construction under 1.5 seconds
        page.evaluate("() => document.getElementById('profile-expertise').scrollIntoView()")
        page.wait_for_timeout(1400) # under 1.5s
        p_state = page.evaluate("() => document.getElementById('profile-expertise').getAttribute('data-nb')")
        print(f"Profile & Expertise state at 1.4s: {p_state}")
        assert p_state in ['pulling', 'built'], f"Expected section to build under 1.5s, got {p_state}"

        # 6. Test Nano AI Chatbot Modal
        page.evaluate("() => { if (window.nanoChat && window.nanoChat.open) window.nanoChat.open(); }")
        page.wait_for_timeout(400)
        modal_open = page.evaluate("() => document.getElementById('nano-chat-modal-overlay').classList.contains('active')")
        print(f"Nano chat modal active: {modal_open}")
        assert modal_open, "Chat modal failed to open"

        page.fill("#nano-input", "Who is Yaser?")
        page.press("#nano-input", "Enter")
        page.wait_for_timeout(500)
        reply = page.evaluate("() => { const msgs = document.querySelectorAll('.nano-msg-row.assistant'); return msgs.length ? msgs[msgs.length - 1].innerText : ''; }")
        print(f"Nano reply: {reply[:60]}...")
        assert len(reply) > 10, "Chat assistant did not reply"
        page.evaluate("() => { if (window.nanoChat && window.nanoChat.close) window.nanoChat.close(); }")
        page.wait_for_timeout(300)

        # 7. Check Error count
        print(f"\nTOTAL PAGE ERRORS: {len(errors)}")
        if errors:
            for e in errors:
                print("ERROR:", e)
        assert len(errors) == 0, f"Encountered page errors: {errors}"

        print("\nALL VERIFICATIONS PASSED WITH 100% SUCCESS!")
        browser.close()

if __name__ == '__main__':
    test()
