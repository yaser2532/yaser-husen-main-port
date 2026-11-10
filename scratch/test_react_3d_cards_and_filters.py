import asyncio
import sys
import json
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: console_errors.append(str(exc)))

        print("Navigating to http://localhost:8080/ ...")
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(2.0)

        # 1. Check React 18 and React3DCard
        react_info = await page.evaluate('''() => {
            return {
                hasReact: typeof React !== 'undefined',
                reactVersion: typeof React !== 'undefined' ? React.version : null,
                hasReactDOM: typeof ReactDOM !== 'undefined',
                hasReact3DCard: typeof window.React3DCard !== 'undefined',
                cardsManaged: window.React3DCard ? window.React3DCard.controllersCount() : 0,
                reactRootPresent: !!document.getElementById('react-3d-root'),
                statusEl: document.getElementById('react-3d-cards-status') ? {
                    version: document.getElementById('react-3d-cards-status').getAttribute('data-react-version'),
                    managed: document.getElementById('react-3d-cards-status').getAttribute('data-cards-managed')
                } : null
            };
        }''')
        print("REACT INFO:", json.dumps(react_info, indent=2))

        # 2. Check Project Filter Buttons stationary styles
        filter_buttons = page.locator('.project-filters .filter-btn')
        count = await filter_buttons.count()
        print(f"Found {count} filter buttons in .project-filters")

        stationary_styles = []
        for i in range(count):
            btn = filter_buttons.nth(i)
            text = (await btn.text_content()).strip()
            style = await btn.evaluate('''(el) => {
                const comp = window.getComputedStyle(el);
                return {
                    text: el.textContent.trim(),
                    bg: comp.backgroundColor,
                    border: comp.borderTopColor,
                    color: comp.color,
                    boxShadow: comp.boxShadow
                };
            }''')
            stationary_styles.append(style)
            print(f"Filter Btn [{text}]: bg={style['bg']}, border={style['border']}, color={style['color']}")

        # Verify all stationary styles match
        first = stationary_styles[0]
        stationary_match = all(
            s['bg'] == first['bg'] and s['border'] == first['border'] and s['color'] == first['color']
            for s in stationary_styles
        )
        print(f"Stationary Filter Buttons Match: {stationary_match}")

        # 3. Check Filter Buttons on Hover
        hover_styles = []
        for i in range(count):
            btn = filter_buttons.nth(i)
            text = (await btn.text_content()).strip()
            await btn.hover()
            await asyncio.sleep(0.3)
            h_style = await btn.evaluate('''(el) => {
                const comp = window.getComputedStyle(el);
                return {
                    text: el.textContent.trim(),
                    bg: comp.backgroundColor,
                    border: comp.borderTopColor,
                    color: comp.color,
                    boxShadow: comp.boxShadow
                };
            }''')
            hover_styles.append(h_style)
            print(f"Hovered Filter Btn [{text}]: bg={h_style['bg']}, border={h_style['border']}, color={h_style['color']}")

        first_hover = hover_styles[0]
        hover_match = all(
            s['bg'] == first_hover['bg'] and s['border'] == first_hover['border'] and s['color'] == first_hover['color']
            for s in hover_styles
        )
        print(f"Hover Filter Buttons Match: {hover_match}")

        # Screenshot of project filters
        filters_container = page.locator('.project-filters')
        await filters_container.scroll_into_view_if_needed()
        await filters_container.screenshot(path='scratch/verified_uniform_filter_buttons.png')

        # 4. Check 3D Card Hover & Removal of Illumination
        first_card = page.locator('.project-card').first
        await first_card.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)

        # Before hover check
        pre_hover = await first_card.evaluate('''(el) => {
            const comp = window.getComputedStyle(el);
            const before = window.getComputedStyle(el, '::before');
            const after = window.getComputedStyle(el, '::after');
            return {
                transform: comp.transform,
                beforeDisplay: before.display,
                beforeOpacity: before.opacity,
                afterDisplay: after.display,
                afterOpacity: after.opacity,
                boxShadow: comp.boxShadow
            };
        }''')
        print("PRE-HOVER CARD:", json.dumps(pre_hover, indent=2))

        # Hover over top-right corner to induce tilt
        box = await first_card.bounding_box()
        # Viewport coordinates for mouse move
        await page.mouse.move(box['x'] + box['width'] * 0.85, box['y'] + box['height'] * 0.25)
        await asyncio.sleep(0.6)

        post_hover = await first_card.evaluate('''(el) => {
            const comp = window.getComputedStyle(el);
            const before = window.getComputedStyle(el, '::before');
            const after = window.getComputedStyle(el, '::after');
            
            // Check inner layers transform
            const layers = Array.from(el.querySelectorAll('.card-3d-layer')).map(l => ({
                tag: l.tagName,
                cls: l.className,
                depth: l.dataset.depth,
                transform: l.style.transform
            }));

            return {
                transform: comp.transform,
                has3DTransform: el.style.transform.includes('perspective') && el.style.transform.includes('rotate'),
                rawTransform: el.style.transform,
                beforeDisplay: before.display,
                beforeOpacity: before.opacity,
                afterDisplay: after.display,
                afterOpacity: after.opacity,
                boxShadow: comp.boxShadow,
                layers: layers.slice(0, 4)
            };
        }''')
        print("POST-HOVER CARD 3D:", json.dumps(post_hover, indent=2))

        # Take screenshot of hovered 3D card
        await first_card.screenshot(path='scratch/verified_3d_card_hover.png')

        # Check projects section
        projects_sec = page.locator('#projects')
        await projects_sec.screenshot(path='scratch/verified_projects_section.png')

        print(f"Console errors: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print("  ERROR:", err)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
