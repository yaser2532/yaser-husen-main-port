import asyncio
from playwright.async_api import async_playwright

async def verify_everything():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        errors = []
        page.on('pageerror', lambda err: errors.append(f"PageError: {err}"))
        
        print("1. Loading portfolio on http://localhost:8080/...")
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await asyncio.sleep(1)
        
        # ----------------------------------------------------
        # TEST 1: Drone Pull Durations in drones.js
        # ----------------------------------------------------
        print("\n--- TEST 1: Dot Elements Pulling Speed ---")
        with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
            djs = f.read()
        assert 'pullDuration = 280;' in djs, "Card pullDuration is not 280ms"
        assert 'pullDuration = 500;' in djs, "Title pullDuration is not 500ms"
        assert 'pullDuration = 350;' in djs, "Paragraph pullDuration is not 350ms"
        assert 'pullDuration = 250;' in djs, "Button pullDuration is not 250ms"
        print("PASS: Drone element pull speed reduced by 0.1s (Card: 280ms, Title: 500ms, Para: 350ms, Btn: 250ms)")

        # ----------------------------------------------------
        # TEST 2: Glitched-out Gradient Hover on Buttons
        # ----------------------------------------------------
        print("\n--- TEST 2: Glitched-out Gradient Hover on Buttons ---")
        hero_btn = page.locator('.hero-actions .cta-button, .cta-button').first
        await hero_btn.scroll_into_view_if_needed()
        box_btn = await hero_btn.bounding_box()
        
        # Hover over button
        await page.mouse.move(box_btn['x'] + box_btn['width'] / 2, box_btn['y'] + box_btn['height'] / 2)
        await asyncio.sleep(0.3)
        
        btn_hover_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                background: cs.background,
                backgroundImage: cs.backgroundImage,
                boxShadow: cs.boxShadow,
                borderColor: cs.borderColor,
                animationName: cs.animationName,
                color: cs.color
            };
        }''', await hero_btn.element_handle())
        
        print("Hero CTA Button Hover Data:")
        print("  backgroundImage:", btn_hover_data['backgroundImage'][:80])
        print("  boxShadow:", btn_hover_data['boxShadow'])
        print("  borderColor:", btn_hover_data['borderColor'])
        print("  animationName:", btn_hover_data['animationName'])
        
        assert 'linear-gradient' in btn_hover_data['backgroundImage'], "Button background does not contain linear-gradient"
        assert 'heroCharGradientShift' in btn_hover_data['animationName'], "Button does not have heroCharGradientShift animation"
        assert 'btnGlitchJitter' in btn_hover_data['animationName'], "Button does not have btnGlitchJitter animation"
        
        await hero_btn.screenshot(path='scratch/verified_button_glitched_hover.png')
        print("Saved screenshot to scratch/verified_button_glitched_hover.png")
        print("PASS: Button exhibits hero-name glitched-out animated gradient hover effect!")

        # ----------------------------------------------------
        # TEST 3: Glitched-out Gradient Hover on Navbar Links
        # ----------------------------------------------------
        print("\n--- TEST 3: Glitched-out Gradient Hover on Navbar Links ---")
        nav_link = page.locator('header nav a, .nav-link').first
        nav_box = await nav_link.bounding_box()
        
        await page.mouse.move(nav_box['x'] + nav_box['width'] / 2, nav_box['y'] + nav_box['height'] / 2)
        await asyncio.sleep(0.3)
        
        nav_hover_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                backgroundImage: cs.backgroundImage,
                webkitBackgroundClip: cs.webkitBackgroundClip,
                animationName: cs.animationName,
                filter: cs.filter
            };
        }''', await nav_link.element_handle())
        
        print("Navbar Link Hover Data:")
        print("  backgroundImage:", nav_hover_data['backgroundImage'][:80])
        print("  webkitBackgroundClip:", nav_hover_data['webkitBackgroundClip'])
        print("  animationName:", nav_hover_data['animationName'])
        print("  filter:", nav_hover_data['filter'])
        
        assert 'linear-gradient' in nav_hover_data['backgroundImage'], "Navbar link does not have linear-gradient background"
        assert nav_hover_data['webkitBackgroundClip'] == 'text', "Navbar link does not clip background to text"
        assert 'heroCharGradientShift' in nav_hover_data['animationName'], "Navbar link missing heroCharGradientShift"
        assert 'navLinkGlitch' in nav_hover_data['animationName'], "Navbar link missing navLinkGlitch"
        
        await page.locator('header').screenshot(path='scratch/verified_navbar_glitched_hover.png')
        print("Saved screenshot to scratch/verified_navbar_glitched_hover.png")
        print("PASS: Navbar links exhibit hero-name glitched-out gradient hover effect!")

        # ----------------------------------------------------
        # TEST 4: Card Elements Pop-Up Behavior on Hover
        # ----------------------------------------------------
        print("\n--- TEST 4: Card Elements Pop-Up Behavior on Hover ---")
        card = page.locator('.project-card').first
        await card.scroll_into_view_if_needed()
        await page.evaluate("window.scrollBy(0, 150)")
        
        # Wait for drone assembly
        await page.wait_for_function("() => document.querySelector('.project-card')?.getAttribute('data-drone-state') === 'built'")
        
        card_box = await card.bounding_box()
        # Hover center of card
        await page.mouse.move(card_box['x'] + card_box['width'] / 2, card_box['y'] + card_box['height'] / 2, steps=6)
        await asyncio.sleep(0.4)
        
        card_hover_data = await page.evaluate('''(el) => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                inlineTransform: el.style.transform,
                boxShadow: cs.boxShadow,
                borderColor: cs.borderColor,
                backdropFilter: cs.backdropFilter || cs.webkitBackdropFilter,
                backgroundColor: cs.backgroundColor
            };
        }''', await card.element_handle())
        
        print("Card Hover Data:")
        print("  inlineTransform:", card_hover_data['inlineTransform'])
        print("  computedTransform:", card_hover_data['transform'])
        print("  boxShadow:", card_hover_data['boxShadow'])
        print("  borderColor:", card_hover_data['borderColor'])
        print("  backdropFilter:", card_hover_data['backdropFilter'])
        
        assert 'matrix3d' in card_hover_data['transform'], "Card does not have 3D matrix transform"
        assert 'rgb(25, 227, 209)' in card_hover_data['borderColor'], "Card border does not match cyber turquoise #19E3D1"
        assert 'blur(14px)' in card_hover_data['backdropFilter'], "Card missing frosted backdrop-filter blur"
        
        await card.screenshot(path='scratch/verified_card_popup_hover.png')
        print("Saved screenshot to scratch/verified_card_popup_hover.png")
        print("PASS: Card element pops up with spring elevation, cyber turquoise border, and deep shadow!")

        # ----------------------------------------------------
        # TEST 5: Card Elements Pop-Up Modal Window on Click
        # ----------------------------------------------------
        print("\n--- TEST 5: Card Elements Click Pop-Up Modal Window ---")
        # Click the card to open pop-up modal lightbox window
        await card.click(position={'x': 30, 'y': 30})
        await asyncio.sleep(0.5)
        
        modal_data = await page.evaluate('''() => {
            const overlay = document.getElementById('card-popup-modal-overlay');
            const win = overlay ? overlay.querySelector('.card-popup-window') : null;
            const title = overlay ? overlay.querySelector('.card-popup-title') : null;
            const csOverlay = overlay ? window.getComputedStyle(overlay) : null;
            const csWin = win ? window.getComputedStyle(win) : null;
            return {
                overlayExists: !!overlay,
                overlayActive: overlay ? overlay.classList.contains('active') : false,
                overlayVisibility: csOverlay ? csOverlay.visibility : null,
                overlayOpacity: csOverlay ? csOverlay.opacity : null,
                windowTransform: csWin ? csWin.transform : null,
                modalTitleText: title ? title.textContent : null
            };
        }''')
        
        print("Card Pop-Up Modal Window State:")
        print("  overlayActive:", modal_data['overlayActive'])
        print("  overlayVisibility:", modal_data['overlayVisibility'])
        print("  overlayOpacity:", modal_data['overlayOpacity'])
        print("  windowTransform:", modal_data['windowTransform'])
        print("  modalTitleText:", modal_data['modalTitleText'])
        
        assert modal_data['overlayActive'] == True, "Card modal overlay is not active"
        assert modal_data['overlayVisibility'] == 'visible', "Card modal overlay is not visible"
        assert float(modal_data['overlayOpacity']) > 0.9, "Card modal overlay opacity is not 1"
        assert 'matrix' in modal_data['windowTransform'], "Modal window did not apply pop-up transform"
        
        await page.screenshot(path='scratch/verified_card_popup_modal_window.png')
        print("Saved screenshot to scratch/verified_card_popup_modal_window.png")
        
        # Test Close Modal with Escape
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.4)
        closed_data = await page.evaluate('''() => {
            const overlay = document.getElementById('card-popup-modal-overlay');
            return overlay ? overlay.classList.contains('active') : false;
        }''')
        print("Modal closed after Esc key:", not closed_data)
        assert closed_data == False, "Card modal overlay failed to close on Esc key"
        print("PASS: Card elements behave like the AI chat pop-up window on both hover and click!")

        # ----------------------------------------------------
        # TEST 6: Responsiveness Across All Screen Sizes
        # ----------------------------------------------------
        print("\n--- TEST 6: Overall Website Responsiveness ---")
        viewports = [
            ('mobile_320', 320, 600),
            ('mobile_375', 375, 667),
            ('mobile_414', 414, 896),
            ('tablet_768', 768, 1024),
            ('tablet_1024', 1024, 768),
            ('desktop_1440', 1440, 900),
            ('desktop_1920', 1920, 1080)
        ]
        
        for name, w, h in viewports:
            await page.set_viewport_size({'width': w, 'height': h})
            await asyncio.sleep(0.3)
            overflow = await page.evaluate('''() => {
                return {
                    scrollWidth: document.documentElement.scrollWidth,
                    windowWidth: window.innerWidth,
                    hasOverflow: document.documentElement.scrollWidth > window.innerWidth
                };
            }''')
            print(f"  {name:12} ({w:4}x{h:4}): hasOverflow={overflow['hasOverflow']}")
            assert overflow['hasOverflow'] == False, f"Horizontal overflow detected on {name}"
        
        print("PASS: Zero horizontal overflow on all 7 viewport sizes!")
        
        assert len(errors) == 0, f"Encountered page errors: {errors}"
        print(f"\nALL SUITE TESTS PASSED WITH 0 ERRORS!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify_everything())
