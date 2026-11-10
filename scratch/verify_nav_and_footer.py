import time
from playwright.sync_api import sync_playwright

def main():
    print("Starting Navbar & Footer verification...")
    errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # ─── PART 1: DESKTOP NAVBAR & FOOTER (1440x900) ───
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))
        
        page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(1.0)
        
        # Navbar Desktop Initial Measurement
        navbar = page.query_selector("#navbar")
        assert navbar is not None, "Navbar should exist"
        nav_bbox = navbar.bounding_box()
        print(f"Desktop Navbar Initial Bounding Box: {nav_bbox}")
        assert nav_bbox["height"] <= 65, f"Desktop navbar initial height should be <= 65px, got {nav_bbox['height']}"
        
        # Test Link Hover
        first_link = page.query_selector(".nav-link")
        l_bbox = first_link.bounding_box()
        page.mouse.move(l_bbox["x"] + l_bbox["width"]/2, l_bbox["y"] + l_bbox["height"]/2)
        time.sleep(0.3)
        page.query_selector("nav").screenshot(path="scratch/test_nav_desktop_hover.png")
        print("Captured scratch/test_nav_desktop_hover.png")
        
        # Test Scroll and Navbar Scrolled State
        page.evaluate("window.scrollTo(0, 300)")
        time.sleep(0.5)
        is_scrolled = page.evaluate("document.getElementById('navbar').classList.contains('scrolled')")
        print(f"Navbar scrolled class active: {is_scrolled}")
        assert is_scrolled, "Navbar should have 'scrolled' class after scrolling 300px"
        scrolled_bbox = navbar.bounding_box()
        print(f"Scrolled Navbar Bounding Box: {scrolled_bbox}")
        assert scrolled_bbox["height"] <= 58, f"Scrolled navbar height should be <= 58px, got {scrolled_bbox['height']}"
        page.query_selector("nav").screenshot(path="scratch/test_nav_scrolled.png")
        print("Captured scratch/test_nav_scrolled.png")
        
        # Test Footer Measurement
        print("\n--- Footer Height Check ---")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.0)
        footer = page.query_selector("footer#contact")
        assert footer is not None, "Footer should exist"
        footer_bbox = footer.bounding_box()
        print(f"Footer Bounding Box: {footer_bbox}")
        # The overall footer padding was decreased to 0.65rem top + 0.85rem bottom
        assert footer_bbox["height"] <= 100, f"Footer height should be <= 100px, got {footer_bbox['height']}"
        
        footer.screenshot(path="scratch/test_footer_compact_dock.png")
        print("Captured scratch/test_footer_compact_dock.png")
        page.close()
        context.close()
        
        # ─── PART 2: TABLET VIEWPORT (820x1180 - iPad Air) ───
        print("\n--- Tablet Viewport Check (820px) ---")
        tab_context = browser.new_context(viewport={"width": 820, "height": 1180})
        tab_page = tab_context.new_page()
        tab_page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(0.8)
        
        # In tablet mode, burger should be visible and navigation drawer responsive
        burger = tab_page.query_selector(".burger")
        assert burger is not None, "Burger menu should exist"
        burger_vis = tab_page.evaluate("window.getComputedStyle(document.querySelector('.burger')).display !== 'none'")
        print(f"Tablet Burger visible: {burger_vis}")
        assert burger_vis, "Burger should be visible at 820px viewport"
        
        # Click burger to open drawer
        burger.click()
        time.sleep(0.4)
        is_open = tab_page.evaluate("document.querySelector('.nav-container').classList.contains('nav-active')")
        print(f"Drawer is open: {is_open}")
        assert is_open, "Drawer should be open after clicking burger"
        
        tab_page.screenshot(path="scratch/test_nav_tablet_drawer_open.png")
        print("Captured scratch/test_nav_tablet_drawer_open.png")
        
        # Press Escape to close
        tab_page.keyboard.press("Escape")
        time.sleep(0.3)
        is_closed = tab_page.evaluate("!document.querySelector('.nav-container').classList.contains('nav-active')")
        print(f"Drawer closed on Escape: {is_closed}")
        assert is_closed, "Drawer should close on Escape key"
        
        tab_page.close()
        tab_context.close()
        
        # ─── PART 3: MOBILE VIEWPORT (375x667 - iPhone SE) ───
        print("\n--- Mobile Viewport Check (375px) ---")
        mob_context = browser.new_context(viewport={"width": 375, "height": 667})
        mob_page = mob_context.new_page()
        mob_page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(0.8)
        
        # Test mobile burger toggle
        mob_burger = mob_page.query_selector(".burger")
        mob_burger.click()
        time.sleep(0.4)
        mob_page.screenshot(path="scratch/test_nav_mobile_drawer_open.png")
        print("Captured scratch/test_nav_mobile_drawer_open.png")
        
        # Test clicking link closes drawer
        first_mob_link = mob_page.query_selector(".nav-links a")
        first_mob_link.click()
        time.sleep(0.3)
        mob_closed = mob_page.evaluate("!document.querySelector('.nav-container').classList.contains('nav-active')")
        print(f"Drawer closed after link click: {mob_closed}")
        assert mob_closed, "Drawer should close after clicking a nav link"
        
        # Check mobile footer
        mob_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.8)
        mob_footer = mob_page.query_selector("footer#contact")
        mob_footer_bbox = mob_footer.bounding_box()
        print(f"Mobile Footer Bounding Box: {mob_footer_bbox}")
        mob_footer.screenshot(path="scratch/test_footer_mobile.png")
        print("Captured scratch/test_footer_mobile.png")
        
        mob_page.close()
        mob_context.close()
        
        print("\n--- Console Errors Audit ---")
        print(f"Total console errors encountered: {len(errors)}")
        if errors:
            for e in errors:
                print("  ERROR:", e)
        assert len(errors) == 0, "Encountered console errors!"
        print("PASS: 0 Console Errors!")
        
        browser.close()
        print("\nNavbar & Footer verification successfully completed!")

if __name__ == "__main__":
    main()
