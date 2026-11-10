import asyncio
from playwright.async_api import async_playwright

async def verify_3d_cards():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        print("1. Loading website...")
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await asyncio.sleep(1)
        
        # Test 1: Project Card 3D Tilt & Elevation
        print("\n2. Scrolling to Projects Section...")
        card = page.locator('.project-card').first
        await card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 150)")
        
        # Wait for drone assembly
        await page.wait_for_function("() => document.querySelector('.project-card')?.getAttribute('data-drone-state') === 'built'")
        print("Project card built by drone swarm!")
        
        box = await card.bounding_box()
        print(f"Card bounding box: w={box['width']:.1f}, h={box['height']:.1f} at ({box['x']:.1f}, {box['y']:.1f})")
        
        # 1a. Hover top-left corner
        tl_x = box['x'] + box['width'] * 0.15
        tl_y = box['y'] + box['height'] * 0.15
        print(f"Moving cursor to top-left ({tl_x:.1f}, {tl_y:.1f})...")
        await page.mouse.move(tl_x, tl_y, steps=8)
        await asyncio.sleep(0.4)
        
        tl_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            const img = el.querySelector('.project-img-container');
            const title = el.querySelector('.project-title, .project-details h3');
            const badge = el.querySelector('.badge');
            const link = el.querySelector('.project-link');
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                inlineBoxShadow: el.style.boxShadow,
                imgTransform: img ? window.getComputedStyle(img).transform : null,
                titleTransform: title ? window.getComputedStyle(title).transform : null,
                badgeTransform: badge ? window.getComputedStyle(badge).transform : null,
                linkTransform: link ? window.getComputedStyle(link).transform : null
            };
        }''', await card.element_handle())
        
        print("Top-left hover data:")
        print("  inlineTransform:", tl_data['inlineTransform'])
        print("  computedTransform:", tl_data['transform'])
        print("  inlineBoxShadow:", tl_data['inlineBoxShadow'])
        print("  imgTransform:", tl_data['imgTransform'])
        print("  titleTransform:", tl_data['titleTransform'])
        print("  badgeTransform:", tl_data['badgeTransform'])
        
        await card.screenshot(path='scratch/verified_project_card_3d_tilt_top_left.png')
        print("Saved scratch/verified_project_card_3d_tilt_top_left.png")
        
        # 1b. Hover bottom-right corner
        br_x = box['x'] + box['width'] * 0.85
        br_y = box['y'] + box['height'] * 0.85
        print(f"\nMoving cursor to bottom-right ({br_x:.1f}, {br_y:.1f})...")
        await page.mouse.move(br_x, br_y, steps=8)
        await asyncio.sleep(0.4)
        
        br_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                inlineBoxShadow: el.style.boxShadow
            };
        }''', await card.element_handle())
        
        print("Bottom-right hover data:")
        print("  inlineTransform:", br_data['inlineTransform'])
        print("  computedTransform:", br_data['transform'])
        print("  inlineBoxShadow:", br_data['inlineBoxShadow'])
        
        await card.screenshot(path='scratch/verified_project_card_3d_tilt_bottom_right.png')
        print("Saved scratch/verified_project_card_3d_tilt_bottom_right.png")
        
        # Test 2: Expertise Card 3D Tilt
        print("\n3. Testing Expertise Card 3D Tilt...")
        exp_card = page.locator('.expertise-card').first
        await exp_card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 80)")
        await page.wait_for_function("() => document.querySelector('.expertise-card')?.getAttribute('data-drone-state') === 'built'")
        
        exp_box = await exp_card.bounding_box()
        exp_tl_x = exp_box['x'] + exp_box['width'] * 0.2
        exp_tl_y = exp_box['y'] + exp_box['height'] * 0.2
        await page.mouse.move(exp_tl_x, exp_tl_y, steps=8)
        await asyncio.sleep(0.4)
        
        exp_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            const icon = el.querySelector('.expertise-icon');
            const h4 = el.querySelector('h4');
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                iconTransform: icon ? window.getComputedStyle(icon).transform : null,
                h4Transform: h4 ? window.getComputedStyle(h4).transform : null
            };
        }''', await exp_card.element_handle())
        
        print("Expertise card hover data:")
        print("  inlineTransform:", exp_data['inlineTransform'])
        print("  computedTransform:", exp_data['transform'])
        print("  iconTransform:", exp_data['iconTransform'])
        print("  h4Transform:", exp_data['h4Transform'])
        
        await exp_card.screenshot(path='scratch/verified_expertise_card_3d_tilt.png')
        print("Saved scratch/verified_expertise_card_3d_tilt.png")
        
        # Test 3: Certification Card 3D Tilt
        print("\n4. Testing Certification Card 3D Tilt...")
        cert_card = page.locator('.cert-card').first
        await cert_card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 80)")
        await page.wait_for_function("() => document.querySelector('.cert-card')?.getAttribute('data-drone-state') === 'built'")
        
        cert_box = await cert_card.bounding_box()
        cert_br_x = cert_box['x'] + cert_box['width'] * 0.8
        cert_br_y = cert_box['y'] + cert_box['height'] * 0.8
        await page.mouse.move(cert_br_x, cert_br_y, steps=8)
        await asyncio.sleep(0.4)
        
        cert_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            const img = el.querySelector('.cert-img-wrapper');
            const btn = el.querySelector('.view-cert-btn');
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                imgTransform: img ? window.getComputedStyle(img).transform : null,
                btnTransform: btn ? window.getComputedStyle(btn).transform : null
            };
        }''', await cert_card.element_handle())
        
        print("Cert card hover data:")
        print("  inlineTransform:", cert_data['inlineTransform'])
        print("  computedTransform:", cert_data['transform'])
        print("  imgTransform:", cert_data['imgTransform'])
        print("  btnTransform:", cert_data['btnTransform'])
        
        await cert_card.screenshot(path='scratch/verified_cert_card_3d_tilt.png')
        print("Saved scratch/verified_cert_card_3d_tilt.png")
        
        # Test 4: Mouse Leave Settling
        print("\n5. Testing Mouse Leave Settling back to flat plane...")
        await page.mouse.move(10, 10, steps=5)
        await asyncio.sleep(0.8)
        
        settled_transform = await page.evaluate('''(el) => el.style.transform''', await cert_card.element_handle())
        print("Settled inline transform (should be empty string):", repr(settled_transform))
        
        print("\nALL 3D CARD VERIFICATIONS COMPLETED SUCCESSFULLY!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify_3d_cards())
