import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(1.0)
        
        # Test Nav Resume Button hover
        print("Testing Nav Resume Button Hover...")
        resume_btn = page.query_selector(".nav-resume-btn")
        if resume_btn:
            bbox = resume_btn.bounding_box()
            page.mouse.move(bbox["x"] + bbox["width"]/2, bbox["y"] + bbox["height"]/2)
            time.sleep(0.3)
            resume_btn.screenshot(path="scratch/test_glitch_nav_resume.png")
            print("Captured scratch/test_glitch_nav_resume.png")
        
        # Scroll to Profile Expertise and wait for drones to build it
        print("Scrolling to Profile & Expertise...")
        page.evaluate("window.scrollTo(0, 1100)")
        time.sleep(2.5) # Allow drone build sequence to complete
        
        # Capture Expertise Card Hover
        print("Testing Expertise Card Hover...")
        card = page.query_selector(".expertise-card")
        if card:
            cbbox = card.bounding_box()
            page.mouse.move(cbbox["x"] + cbbox["width"]/2, cbbox["y"] + cbbox["height"]/2)
            time.sleep(0.4)
            card.screenshot(path="scratch/test_glitch_expertise_card.png")
            print("Captured scratch/test_glitch_expertise_card.png")
            
        # Scroll to Projects Section and wait for drone build sequence
        print("Scrolling to Projects...")
        page.evaluate("window.scrollTo(0, 2400)")
        time.sleep(3.0)
        
        # Capture Filter Button Hover
        filter_btn = page.query_selector('.filter-btn[data-filter="ai-data"]')
        if filter_btn:
            fbbox = filter_btn.bounding_box()
            page.mouse.move(fbbox["x"] + fbbox["width"]/2, fbbox["y"] + fbbox["height"]/2)
            time.sleep(0.3)
            filter_btn.screenshot(path="scratch/test_glitch_filter_btn.png")
            print("Captured scratch/test_glitch_filter_btn.png")
            
        # Capture Project Card with Holo Sticker Hover
        p_card = page.query_selector(".project-card")
        if p_card:
            pbbox = p_card.bounding_box()
            page.mouse.move(pbbox["x"] + pbbox["width"]/2, pbbox["y"] + pbbox["height"]/2)
            time.sleep(0.4)
            p_card.screenshot(path="scratch/test_glitch_project_card.png")
            print("Captured scratch/test_glitch_project_card.png")
            
            # Hover over the project link inside the card
            p_link = p_card.query_selector(".project-link")
            if p_link:
                pl_bbox = p_link.bounding_box()
                page.mouse.move(pl_bbox["x"] + pl_bbox["width"]/2, pl_bbox["y"] + pl_bbox["height"]/2)
                time.sleep(0.3)
                p_link.screenshot(path="scratch/test_glitch_project_link.png")
                print("Captured scratch/test_glitch_project_link.png")
                
        # Scroll down to Footer and test dock buttons
        print("Scrolling to Footer...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2.0)
        dock_btn = page.query_selector(".dock-btn-contact")
        if dock_btn:
            d_bbox = dock_btn.bounding_box()
            page.mouse.move(d_bbox["x"] + d_bbox["width"]/2, d_bbox["y"] + d_bbox["height"]/2)
            time.sleep(0.3)
            dock_btn.screenshot(path="scratch/test_glitch_dock_btn.png")
            print("Captured scratch/test_glitch_dock_btn.png")

        browser.close()
        print("Finished test_glitched_card_hover!")

if __name__ == "__main__":
    main()
