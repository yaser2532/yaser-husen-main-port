import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        page.goto("http://localhost:8080/", wait_until="networkidle")
        time.sleep(1.0)
        
        # Mark all as built so we can inspect all visual hover states instantly
        page.evaluate("""() => {
            document.querySelectorAll('[data-drone-state]').forEach(el => {
                el.setAttribute('data-drone-state', 'built');
                el.style.opacity = '1';
                el.style.transform = '';
                el.style.filter = '';
            });
        }""")
        time.sleep(0.5)
        
        # 1. Project Card with Holo Sticker Hover
        page.evaluate("document.getElementById('projects').scrollIntoView()")
        time.sleep(0.5)
        
        p_card = page.query_selector(".project-card")
        if p_card:
            pbbox = p_card.bounding_box()
            page.mouse.move(pbbox["x"] + pbbox["width"]/2, pbbox["y"] + pbbox["height"]/2)
            time.sleep(0.4)
            p_card.screenshot(path="scratch/showcase_project_card_hover.png")
            print("Captured scratch/showcase_project_card_hover.png")
            
            # Hover Try It link
            p_link = p_card.query_selector(".project-link")
            if p_link:
                pl_bbox = p_link.bounding_box()
                page.mouse.move(pl_bbox["x"] + pl_bbox["width"]/2, pl_bbox["y"] + pl_bbox["height"]/2)
                time.sleep(0.3)
                p_link.screenshot(path="scratch/showcase_project_link_hover.png")
                print("Captured scratch/showcase_project_link_hover.png")
                
        # 2. Filter Button Hover
        filter_btn = page.query_selector('.filter-btn[data-filter="ai-data"]')
        if filter_btn:
            fbbox = filter_btn.bounding_box()
            page.mouse.move(fbbox["x"] + fbbox["width"]/2, fbbox["y"] + fbbox["height"]/2)
            time.sleep(0.3)
            filter_btn.screenshot(path="scratch/showcase_filter_btn_hover.png")
            print("Captured scratch/showcase_filter_btn_hover.png")
            
        # 3. Full Projects Section Screenshot showing Telemetry Badge + Holo Stickers + Filters
        proj_sec = page.query_selector("#projects")
        if proj_sec:
            proj_sec.screenshot(path="scratch/showcase_projects_section.png")
            print("Captured scratch/showcase_projects_section.png")
            
        browser.close()
        print("Showcase capture complete.")

if __name__ == "__main__":
    main()
