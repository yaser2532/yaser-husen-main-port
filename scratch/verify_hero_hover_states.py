import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))
        
        print("Loading http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        # 1. Hover on UTC clock pill
        clock_pill = await page.query_selector('#hero-live-clock')
        assert clock_pill, "clock_pill found"
        
        await clock_pill.hover()
        await page.wait_for_timeout(350)
        
        clock_hover_style = await clock_pill.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                cursor: cs.cursor,
                transform: cs.transform,
                boxShadow: cs.boxShadow,
                color: cs.color,
                borderColor: cs.borderColor
            };
        }''')
        print("Clock pill hover computed style:", clock_hover_style)
        assert clock_hover_style['cursor'] == 'pointer', "Cursor should be pointer on UTC clock"
        assert clock_hover_style['transform'] != 'none', "Transform should be active on hover"
        
        clock_shot = os.path.join(ARTIFACT_DIR, 'hover_hero_utc_clock.png')
        await page.screenshot(path=clock_shot)
        print("Saved hover_hero_utc_clock.png!")
        
        # 2. Click UTC clock pill to toggle to Local time
        await clock_pill.click()
        await page.wait_for_timeout(300)
        clock_text = await page.evaluate('''() => document.getElementById('clock-utc').textContent''')
        print("Clock text after click:", clock_text)
        assert 'LOCAL' in clock_text, "Clicking clock pill should toggle to LOCAL time"
        
        # 3. Hover on Hero Sticker Badge (Status Intel)
        badge = await page.query_selector('.hero-sticker-badge')
        await badge.hover()
        await page.wait_for_timeout(350)
        badge_hover_style = await badge.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                cursor: cs.cursor,
                transform: cs.transform,
                boxShadow: cs.boxShadow
            };
        }''')
        print("Badge hover style:", badge_hover_style)
        assert badge_hover_style['cursor'] == 'pointer', "Badge cursor should be pointer"
        
        badge_shot = os.path.join(ARTIFACT_DIR, 'hover_hero_status_badge.png')
        await page.screenshot(path=badge_shot)
        print("Saved hover_hero_status_badge.png!")
        
        # 4. Hover on Hero Spec Stamp
        stamp = await page.query_selector('.hero-spec-stamp')
        await stamp.hover()
        await page.wait_for_timeout(350)
        stamp_hover_style = await stamp.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                cursor: cs.cursor,
                transform: cs.transform,
                boxShadow: cs.boxShadow,
                letterSpacing: cs.letterSpacing
            };
        }''')
        print("Stamp hover style:", stamp_hover_style)
        assert stamp_hover_style['cursor'] == 'pointer', "Stamp cursor should be pointer"
        
        stamp_shot = os.path.join(ARTIFACT_DIR, 'hover_hero_spec_stamp.png')
        await page.screenshot(path=stamp_shot)
        print("Saved hover_hero_spec_stamp.png!")
        
        # 5. Check all 6 responsive viewports
        viewports = [320, 375, 768, 1024, 1440, 2560]
        overflows = {}
        for vp in viewports:
            await page.set_viewport_size({'width': vp, 'height': 800})
            await page.wait_for_timeout(100)
            sw, cw = await page.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
            overflows[vp] = max(0, sw - cw)
            
        print("Overflows across viewports:", overflows)
        assert all(v == 0 for v in overflows.values()), "0 horizontal overflow"
        
        print("Console errors:", console_errors)
        assert len(console_errors) == 0, "0 console errors"
        
        await browser.close()
        print("\nAll Hero Hover & UTC Tests PASSED 100%!")

if __name__ == '__main__':
    asyncio.run(main())
