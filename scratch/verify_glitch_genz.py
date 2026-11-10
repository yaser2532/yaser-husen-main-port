import sys
import time
from playwright.sync_api import sync_playwright

def main():
    print("Starting Glitch and Gen Z verification...")
    errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.0
        )
        page = context.new_page()
        
        # Track console errors
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))
        
        t0 = time.time()
        page.goto("http://localhost:8080/", wait_until="networkidle")
        load_time = (time.time() - t0) * 1000
        print(f"Page loaded in {load_time:.1f}ms")
        
        time.sleep(1.0)
        
        # Test 1: Hero Name Letters Glitched Gradient Effect
        print("\n--- Test 1: Hero Name Letters Glitched Gradient Effect ---")
        chars = page.query_selector_all(".hero-3d-char")
        print(f"Found {len(chars)} hero 3d characters.")
        assert len(chars) >= 10, "Expected at least 10 letters for YASER HUSEN"
        
        # Hover over first char 'Y'
        first_char = page.query_selector('.hero-3d-char[data-char="Y"]')
        assert first_char is not None, "First char 'Y' not found"
        
        bbox = first_char.bounding_box()
        print(f"Char 'Y' bounding box: {bbox}")
        page.mouse.move(bbox["x"] + bbox["width"]/2, bbox["y"] + bbox["height"]/2)
        time.sleep(0.3)
        
        # Capture screenshot of hero name with hovered char
        hero_title = page.query_selector(".hero-title")
        hero_title.screenshot(path="scratch/test_glitch_hero_char.png")
        print("Captured scratch/test_glitch_hero_char.png")
        
        # Test 2: Buttons Glitched-Out Color Gradient Effect
        print("\n--- Test 2: Buttons Glitched Color Gradient Effect ---")
        cta_btn = page.query_selector(".cta-button")
        assert cta_btn is not None, "CTA button not found"
        
        cta_bbox = cta_btn.bounding_box()
        page.mouse.move(cta_bbox["x"] + cta_bbox["width"]/2, cta_bbox["y"] + cta_bbox["height"]/2)
        time.sleep(0.3)
        
        cta_btn.screenshot(path="scratch/test_glitch_cta_btn.png")
        print("Captured scratch/test_glitch_cta_btn.png")
        
        # Test 3: Kinetic Marquee Ticker Strip
        print("\n--- Test 3: Gen Z Kinetic Marquee Ticker Strip ---")
        marquee = page.query_selector(".cyber-marquee-section")
        assert marquee is not None, "Kinetic marquee not found"
        marquee_bbox = marquee.bounding_box()
        print(f"Marquee bounding box: {marquee_bbox}")
        assert marquee_bbox["height"] > 20, "Marquee has valid height"
        
        # Scroll down slightly to view marquee and horizon transition
        page.evaluate("window.scrollTo(0, 500)")
        time.sleep(0.6)
        page.screenshot(path="scratch/test_kinetic_marquee.png")
        print("Captured scratch/test_kinetic_marquee.png")
        
        # Test 4: Project Card Glitched Gradient Hover
        print("\n--- Test 4: Project Card Glitched Hover ---")
        page.evaluate("document.getElementById('projects').scrollIntoView()")
        time.sleep(0.8)
        
        card = page.query_selector(".project-card")
        assert card is not None, "Project card not found"
        card_bbox = card.bounding_box()
        page.mouse.move(card_bbox["x"] + card_bbox["width"]/2, card_bbox["y"] + card_bbox["height"]/2)
        time.sleep(0.4)
        
        card.screenshot(path="scratch/test_glitch_card.png")
        print("Captured scratch/test_glitch_card.png")
        
        # Test 5: Links Glitched Gradient Hover
        print("\n--- Test 5: Links Glitched Hover ---")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        nav_link = page.query_selector("a.nav-link")
        assert nav_link is not None, "Nav link not found"
        link_bbox = nav_link.bounding_box()
        page.mouse.move(link_bbox["x"] + link_bbox["width"]/2, link_bbox["y"] + link_bbox["height"]/2)
        time.sleep(0.3)
        
        nav_bar = page.query_selector("nav")
        nav_bar.screenshot(path="scratch/test_glitch_nav_links.png")
        print("Captured scratch/test_glitch_nav_links.png")
        
        # Test 6: Filter Buttons Glitch Hover
        print("\n--- Test 6: Filter Buttons Glitch Hover ---")
        page.evaluate("document.getElementById('projects').scrollIntoView()")
        time.sleep(0.6)
        filter_btn = page.query_selector('.filter-btn[data-filter="ai-data"]')
        assert filter_btn is not None, "Filter button not found"
        f_bbox = filter_btn.bounding_box()
        page.mouse.move(f_bbox["x"] + f_bbox["width"]/2, f_bbox["y"] + f_bbox["height"]/2)
        time.sleep(0.3)
        
        filters_container = page.query_selector(".project-filters")
        filters_container.screenshot(path="scratch/test_glitch_filters.png")
        print("Captured scratch/test_glitch_filters.png")
        
        # Check overall errors
        print("\n--- Console Error Audit ---")
        print(f"Total console errors encountered: {len(errors)}")
        if errors:
            for err in errors:
                print("  ERROR:", err)
        else:
            print("  PASS: 0 Console Errors!")
            
        browser.close()
        print("\nVerification successfully finished!")

if __name__ == "__main__":
    main()
