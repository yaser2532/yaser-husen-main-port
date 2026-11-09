import sys
import time
from playwright.sync_api import sync_playwright

def run_tests():
    errors = []
    logs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(str(err)))
        
        print("Navigating to http://localhost:8080/...")
        page.goto("http://localhost:8080/", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        # 1. Check Hero 3D Spherical Core removal
        hero_group_state = page.evaluate("() => window.__gl ? window.__gl.heroGroup : 'no-gl'")
        print(f"window.__gl.heroGroup: {hero_group_state}")
        assert hero_group_state is None, f"Expected heroGroup to be None/null, got {hero_group_state}"
        
        # 2. Check 3D Drones
        drones_count = page.evaluate("() => window.__gl && window.__gl.drones ? window.__gl.drones.length : 0")
        print(f"3D Drones count: {drones_count}")
        assert drones_count == 8, f"Expected 8 drones, got {drones_count}"
        
        # 3. Check Swarm phase API
        swarm_phase = page.evaluate("() => window.swarm ? window.swarm.getPhase() : 'no-swarm'")
        print(f"Swarm initial phase: {swarm_phase}")
        assert swarm_phase in ['idle', 'scout', 'pull'], f"Unexpected swarm phase: {swarm_phase}"
        
        # 4. Check SectionCoordinator
        coord_exists = page.evaluate("() => typeof window.SectionCoordinator !== 'undefined'")
        print(f"SectionCoordinator exists: {coord_exists}")
        assert coord_exists, "SectionCoordinator must exist"
        
        # 5. Check Initial Hero Assembly
        hero_state = page.evaluate("() => document.getElementById('home').getAttribute('data-nb')")
        print(f"Hero section data-nb: {hero_state}")
        assert hero_state == 'built', f"Hero must be built on load, got {hero_state}"
        
        # 6. Test Momentum Scrolling and Scroll-Past Auto-Recovery
        print("\n--- Testing Smooth Momentum Scroll & Auto-Recovery ---")
        # Scroll to 1800 (profile-expertise scrolled past, about-me entering viewport)
        page.evaluate("() => window.glideScrollTo ? window.glideScrollTo(1800) : window.scrollTo(0, 1800)")
        page.wait_for_timeout(1500)
        
        p_state = page.evaluate("() => document.getElementById('profile-expertise').getAttribute('data-nb')")
        a_state = page.evaluate("() => document.getElementById('about-me').getAttribute('data-nb')")
        print(f"Scrolled past profile-expertise: data-nb={p_state}")
        print(f"Entering viewport about-me: data-nb={a_state}")
        assert p_state == 'built', f"profile-expertise must be built when scrolled past, got {p_state}"
        assert a_state in ['scouting', 'pulling', 'built'], f"about-me should be actively processing or built, got {a_state}"
        
        # Scroll down further to 3200 (past about-me, into projects)
        print("\n--- Scrolling past about-me to projects (3200px) ---")
        page.evaluate("() => window.glideScrollTo ? window.glideScrollTo(3200) : window.scrollTo(0, 3200)")
        page.wait_for_timeout(1500)
        a_state_past = page.evaluate("() => document.getElementById('about-me').getAttribute('data-nb')")
        print(f"Scrolled past about-me: data-nb={a_state_past}")
        assert a_state_past == 'built', f"about-me must auto-recover and be built when scrolled past, got {a_state_past}"
        
        # Fast scroll to contact section (jump test)
        print("\n--- Testing Fast Jump to Contact Section ---")
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)
        
        # Verify contact and prior sections
        contact_state = page.evaluate("() => document.getElementById('contact').getAttribute('data-nb')")
        proj_state = page.evaluate("() => document.getElementById('projects').getAttribute('data-nb')")
        cert_state = page.evaluate("() => document.getElementById('certificates').getAttribute('data-nb')")
        print(f"Contact data-nb: {contact_state}")
        print(f"Projects data-nb: {proj_state}")
        print(f"Certificates data-nb: {cert_state}")
        assert proj_state == 'built', f"Projects must be built after scrolling past, got {proj_state}"
        assert cert_state == 'built', f"Certificates must be built after scrolling past, got {cert_state}"
        
        # Scroll back up to profile
        print("\n--- Testing Scroll Back Up to Profile ---")
        page.evaluate("() => window.glideScrollTo ? window.glideScrollTo(1000) : window.scrollTo(0, 1000)")
        page.wait_for_timeout(1500)
        p_state_up = page.evaluate("() => document.getElementById('profile-expertise').getAttribute('data-nb')")
        p_opacity = page.evaluate("() => window.getComputedStyle(document.getElementById('profile-expertise')).opacity")
        print(f"Profile after scrolling up: data-nb={p_state_up}, opacity={p_opacity}")
        assert p_state_up == 'built', f"Profile must stay built when scrolling back, got {p_state_up}"
        assert float(p_opacity) >= 0.9, f"Profile must remain fully visible, opacity is {p_opacity}"
        
        # 7. Test Nano AI Chatbot Modal
        print("\n--- Testing Nano AI Chatbot Modal ---")
        page.evaluate("() => { if (window.nanoChat && window.nanoChat.open) window.nanoChat.open(); }")
        page.wait_for_timeout(600)
        modal_open = page.evaluate("() => document.getElementById('nano-chat-modal-overlay').classList.contains('active')")
        assert modal_open, "Chat modal failed to open"
        
        # Ask a query
        page.fill("#nano-input", "What are your core skills in AI?")
        page.press("#nano-input", "Enter")
        page.wait_for_timeout(800)
        
        # Verify response received
        last_msg = page.evaluate("() => { const msgs = document.querySelectorAll('.nano-msg-bubble.assistant'); return msgs.length ? msgs[msgs.length - 1].innerText : ''; }")
        print(f"Bot response preview: {last_msg[:80]}...")
        assert len(last_msg) > 10, "Bot should return an intelligent response"
        
        # Close chat modal
        page.evaluate("() => { if (window.nanoChat && window.nanoChat.close) window.nanoChat.close(); }")
        page.wait_for_timeout(300)
        
        # 8. Check console errors
        print("\n--- Checking for Console Errors ---")
        critical_errors = [e for e in errors if "favicon" not in e.lower()]
        console_errs = [l for l in logs if l.startswith("[error]") and "favicon" not in l.lower()]
        
        print(f"Page errors: {critical_errors}")
        print(f"Console errors: {console_errs}")
        assert len(critical_errors) == 0, f"Found page errors: {critical_errors}"
        assert len(console_errs) == 0, f"Found console errors: {console_errs}"
        
        print("\n=======================================================")
        print("ALL VERIFICATION TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================")
        browser.close()

if __name__ == "__main__":
    run_tests()
