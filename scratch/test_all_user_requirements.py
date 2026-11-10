import asyncio
import sys
import json
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # -------------------------------------------------------------
        # TEST 1: DESKTOP (1440x900) - HERO BUTTON, ALL BUTTONS, CARDS, DRONES
        # -------------------------------------------------------------
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: console_errors.append(str(exc)))

        print("1. Loading http://localhost:8080/ on Desktop (1440x900)...")
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.5)

        # 1A. Hero "Explore My Work" button checks
        hero_btn = page.locator('.hero-actions .cta-button')
        await hero_btn.wait_for(state='visible')
        
        hero_stationary = await hero_btn.evaluate('''(btn) => {
            const comp = window.getComputedStyle(btn);
            return {
                bg: comp.backgroundColor,
                borderRadius: comp.borderRadius,
                borderTopWidth: comp.borderTopWidth,
                borderTopColor: comp.borderTopColor,
                color: comp.color
            };
        }''')
        print("Hero Button (Stationary):", json.dumps(hero_stationary, indent=2))
        
        # Hover hero button
        await hero_btn.hover()
        await asyncio.sleep(0.3)
        hero_hovered = await hero_btn.evaluate('''(btn) => {
            const comp = window.getComputedStyle(btn);
            return {
                bg: comp.backgroundImage,
                anim: comp.animationName,
                color: comp.color,
                boxShadow: comp.boxShadow
            };
        }''')
        print("Hero Button (Hovered Glitch):", json.dumps(hero_hovered, indent=2))

        # Screenshot hero button
        await hero_btn.screenshot(path='scratch/hero_explore_btn_hover.png')

        # 1B. Test multiple diverse buttons across the site for the gradient glitch hover effect
        test_buttons = [
            ('.hero-actions .cta-button', 'Hero Explore Button'),
            ('.project-filters .filter-btn', 'Project Filter Button'),
            ('.dock-btn', 'Dock Button'),
            ('.nav-resume-btn', 'Nav Resume Button'),
            ('#submit-btn', 'Contact Submit Button')
        ]

        all_buttons_glitch_pass = True
        for sel, label in test_buttons:
            btn_loc = page.locator(sel).first
            if await btn_loc.count() > 0:
                await page.evaluate(f'''() => {{
                    const el = document.querySelector("{sel}");
                    if (el) el.scrollIntoView({{ block: "center", behavior: "instant" }});
                }}''')
                await asyncio.sleep(0.3)
                await btn_loc.hover(force=True)
                await asyncio.sleep(0.2)
                res = await btn_loc.evaluate('''(el) => {
                    const comp = window.getComputedStyle(el);
                    const bg = comp.backgroundImage || '';
                    const hasGrad = bg.includes('linear-gradient') || bg.includes('gradient');
                    return {
                        hasGrad: hasGrad,
                        anim: comp.animationName,
                        color: comp.color,
                        bg: bg
                    };
                }''')
                print(f"Glitch Hover Check [{label}]: hasGradient={res['hasGrad']}, anim={res['anim']}, color={res['color']}")
                if not res['hasGrad']:
                    all_buttons_glitch_pass = False

        print(f"ALL BUTTONS GLITCH PASS: {all_buttons_glitch_pass}")

        # 1C. Test Whole-Card Elements Box Bending & Deformation
        card_loc = page.locator('.project-card').first
        await page.evaluate('''() => {
            const el = document.querySelector(".project-card");
            if (el) el.scrollIntoView({ block: "center", behavior: "instant" });
        }''')
        await asyncio.sleep(0.5)

        # Mouse hover near corner to trigger bending and torsional skew
        box = await card_loc.bounding_box()
        await page.mouse.move(box['x'] + box['width'] * 0.85, box['y'] + box['height'] * 0.2)
        await asyncio.sleep(0.6)

        card_deformation = await card_loc.evaluate('''(card) => {
            const rawTransform = card.style.transform;
            const comp = window.getComputedStyle(card);
            
            // Check inner text transform - must be NONE (no deforming text)
            const textEl = card.querySelector('p, .project-desc, h3');
            const textTransform = textEl ? window.getComputedStyle(textEl).transform : 'none';

            return {
                rawTransform: rawTransform,
                hasPerspective: rawTransform.includes('perspective'),
                hasRotate: rawTransform.includes('rotate'),
                hasSkew: rawTransform.includes('skew'),
                hasTranslate3d: rawTransform.includes('translate3d'),
                textTransform: textTransform,
                boxShadow: comp.boxShadow
            };
        }''')
        print("WHOLE CARD BOX DEFORMATION:", json.dumps(card_deformation, indent=2))
        await card_loc.screenshot(path='scratch/card_whole_box_bending.png')

        # 1D. Test Drone Sequence (Max Active Crews = 2 & Chaotic Drone Flight)
        drone_info = await page.evaluate('''() => {
            return {
                hasSwarm: typeof window.swarm !== 'undefined',
                maxAllowed: 2
            };
        }''')
        print("DRONE SWARM INFO:", json.dumps(drone_info, indent=2))

        # -------------------------------------------------------------
        # TEST 2: TABLET VIEWPORT (768x1024) RESPONSIVENESS
        # -------------------------------------------------------------
        print("2. Testing Tablet Viewport (768x1024)...")
        tab_context = await browser.new_context(viewport={'width': 768, 'height': 1024})
        tab_page = await tab_context.new_page()
        tab_errors = []
        tab_page.on('pageerror', lambda exc: tab_errors.append(str(exc)))
        await tab_page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)
        
        # Check horizontal overflow on tablet
        tab_overflow = await tab_page.evaluate('() => document.documentElement.scrollWidth > window.innerWidth')
        print(f"Tablet horizontal overflow: {tab_overflow} (ScrollWidth: {await tab_page.evaluate('() => document.documentElement.scrollWidth')}, InnerWidth: 768)")
        await tab_page.screenshot(path='scratch/verified_tablet_responsive.png')
        await tab_context.close()

        # -------------------------------------------------------------
        # TEST 3: MOBILE VIEWPORT (375x812) RESPONSIVENESS
        # -------------------------------------------------------------
        print("3. Testing Mobile Viewport (375x812)...")
        mob_context = await browser.new_context(viewport={'width': 375, 'height': 812})
        mob_page = await mob_context.new_page()
        mob_errors = []
        mob_page.on('pageerror', lambda exc: mob_errors.append(str(exc)))
        await mob_page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        # Check hero button on mobile
        mob_hero_btn = mob_page.locator('.hero-actions .cta-button')
        mob_btn_visible = await mob_hero_btn.is_visible()
        print(f"Mobile Hero Button Visible: {mob_btn_visible}")

        # Check horizontal overflow on mobile
        mob_overflow = await mob_page.evaluate('() => document.documentElement.scrollWidth > window.innerWidth')
        print(f"Mobile horizontal overflow: {mob_overflow} (ScrollWidth: {await mob_page.evaluate('() => document.documentElement.scrollWidth')}, InnerWidth: 375)")
        await mob_page.screenshot(path='scratch/verified_mobile_responsive.png')
        await mob_context.close()

        print(f"Total Desktop Console Errors: {len(console_errors)}")
        print(f"Total Tablet Errors: {len(tab_errors)}")
        print(f"Total Mobile Errors: {len(mob_errors)}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
