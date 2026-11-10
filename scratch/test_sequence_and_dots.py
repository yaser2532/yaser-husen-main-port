import asyncio
import math
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))

        print("1. Loading http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await page.wait_for_timeout(600)

        # -------------------------------------------------------------
        # TEST 1: Dot Elements (Neon Glowing Field, Blinking & 2 Hz Gradient Cycle)
        # -------------------------------------------------------------
        dots = await page.locator(".mouse-tracker-dot").all()
        print(f"Total dots found: {len(dots)}")
        assert len(dots) == 8, f"Expected 8 dots, found {len(dots)}"

        # Move mouse to activate dots
        await page.mouse.move(600, 400)
        await page.wait_for_timeout(300)

        # Verify animation property and glow on dots
        dot0_anim = await dots[0].evaluate("el => getComputedStyle(el).animationName")
        dot0_shadow = await dots[0].evaluate("el => getComputedStyle(el).boxShadow")
        print(f"Dot #0 animation: {dot0_anim}")
        print(f"Dot #0 box-shadow (glowing field): {dot0_shadow}")
        assert "dot-neon-gradient-cycle" in dot0_anim, "Dot must have dot-neon-gradient-cycle animation"
        assert "dot-neon-blink" in dot0_anim, "Dot must have dot-neon-blink animation"
        assert len(dot0_shadow) > 10 and dot0_shadow != "none", "Dot must have a neon glowing field"

        # Check that different dots have staggered animation delays
        delays = [await dot.evaluate("el => getComputedStyle(el).animationDelay") for dot in dots[:4]]
        print(f"First 4 dot animation delays: {delays}")
        assert len(set(delays)) > 1, "Dots must have staggered animation delays"

        # -------------------------------------------------------------
        # TEST 2: Halfway Scroll Trigger (NOT triggered prematurely)
        # -------------------------------------------------------------
        pe_sec = page.locator("#profile-expertise")
        pe_state = await pe_sec.evaluate("el => el.getAttribute('data-nb')")
        print(f"Profile-expertise state at page top: '{pe_state}' (Expected 'pending')")
        assert pe_state == "pending", "Section must be pending when visitor is at page top"

        # Scroll just a tiny bit (200px) - NOT halfway into profile-expertise
        await page.evaluate("window.scrollTo({ top: 200, behavior: 'instant' })")
        await page.wait_for_timeout(300)
        pe_state_early = await pe_sec.evaluate("el => el.getAttribute('data-nb')")
        print(f"Profile-expertise state after minor 200px scroll: '{pe_state_early}' (Must remain 'pending')")
        assert pe_state_early == "pending", "Section must NOT trigger before visitor is halfway scrolled!"

        # -------------------------------------------------------------
        # TEST 3: Sequential Element Pull with 0.5s Gap (Title -> Paragraph -> Boxes)
        # -------------------------------------------------------------
        print("Scrolling halfway into Profile & Expertise...")
        # Get section rect and scroll so the section is halfway in view
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const r = sec.getBoundingClientRect();
            window.scrollTo({ top: window.scrollY + r.top - 80, behavior: 'instant' });
        }""")
        # Trigger scroll event
        await page.evaluate("window.dispatchEvent(new Event('scroll'))")

        # Sample at t = 500ms (Title pulling or just assembled, subsequent elements still pending!)
        await page.wait_for_timeout(500)
        nodes_info_500 = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const nodes = Array.from(sec.querySelectorAll('h2.section-title, .section-desc, .profile-card-wrapper, .expertise-card'));
            return nodes.map(n => ({
                tag: n.tagName,
                cls: n.className,
                opacity: getComputedStyle(n).opacity,
                assembled: n.getAttribute('data-assembled')
            }));
        }""")
        print(f"Sample at 500ms: {len(nodes_info_500)} nodes found")
        for i, n in enumerate(nodes_info_500[:4]):
            print(f"  Node #{i} ({n['tag']}.{n['cls'][:15]}): opacity={n['opacity']}, assembled={n['assembled']}")

        # Title (Node #0) should be active/visible, while Node #2, #3 (cards) MUST be opacity 0 (waiting their turn)
        assert float(nodes_info_500[0]['opacity']) > 0.5, "Title (Node #0) must pull first!"
        assert float(nodes_info_500[-1]['opacity']) < 0.2, "Later cards must NOT pull simultaneously (must be waiting)!"

        # Wait another 600ms (t = 1100ms: paragraph is pulled, card 1 starting)
        await page.wait_for_timeout(600)
        nodes_info_1100 = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            const nodes = Array.from(sec.querySelectorAll('h2.section-title, .section-desc, .profile-card-wrapper, .expertise-card'));
            return nodes.map(n => ({
                opacity: getComputedStyle(n).opacity,
                assembled: n.getAttribute('data-assembled')
            }));
        }""")
        print(f"Sample at 1100ms: Node #0 assembled={nodes_info_1100[0]['assembled']}, Node #1 assembled={nodes_info_1100[1]['assembled']}")

        # Wait for full sequence to finish (7 nodes * 0.5s + 0.3s scout = ~4.1s total)
        await page.wait_for_timeout(3500)
        pe_final_state = await pe_sec.evaluate("el => el.getAttribute('data-nb')")
        print(f"Profile-expertise final state: '{pe_final_state}' (Expected 'built')")
        assert pe_final_state == "built", "Section should reach built state after sequential assembly"

        print(f"Console errors: {len(errors)}")
        assert len(errors) == 0, f"Expected 0 console errors, got {errors}"

        # Capture verification screenshot
        await page.screenshot(path="scratch/sequence_and_dots_verified.png")
        print("Screenshot saved to scratch/sequence_and_dots_verified.png")

        await browser.close()
        print("ALL 3 REQUIREMENTS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(verify())
