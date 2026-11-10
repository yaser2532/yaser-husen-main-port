import sys
from playwright.sync_api import sync_playwright

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Button Hover Test
        print("--- 1. Testing Buttons Hover ---", flush=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(300)
        
        hero_btn = page.locator('.hero-actions .cta-button').first
        hero_btn.scroll_into_view_if_needed()
        hero_btn.hover()
        page.wait_for_timeout(200)
        
        hero_style = hero_btn.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.backgroundImage || cs.background,
                textShadow: cs.textShadow,
                boxShadow: cs.boxShadow,
                border: cs.borderColor,
                color: cs.color
            };
        }''')
        print(f"Hero button hovered:\n  textShadow: {hero_style['textShadow']}\n  boxShadow: {hero_style['boxShadow']}\n  color: {hero_style['color']}", flush=True)
        page.screenshot(path='scratch/hero_button_hovered_bloodred.png')
        
        # Project Filter Button Hover
        filter_btn = page.locator('.project-filters .filter-btn').first
        filter_btn.evaluate('el => el.scrollIntoView({ block: "center", behavior: "instant" })')
        filter_btn.hover(force=True)
        page.wait_for_timeout(200)
        filter_style = filter_btn.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.backgroundImage || cs.background,
                textShadow: cs.textShadow,
                boxShadow: cs.boxShadow
            };
        }''')
        print(f"Filter button hovered:\n  textShadow: {filter_style['textShadow']}\n  boxShadow: {filter_style['boxShadow']}", flush=True)
        page.screenshot(path='scratch/filter_button_hovered_bloodred.png')

        # Submit Button Hover
        submit_btn = page.locator('#submit-btn, .btn-submit, button[type="submit"]').first
        submit_btn.evaluate('el => el.scrollIntoView({ block: "center", behavior: "instant" })')
        submit_btn.hover(force=True)
        page.wait_for_timeout(200)
        submit_style = submit_btn.evaluate('''el => {
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.backgroundImage || cs.background,
                textShadow: cs.textShadow,
                boxShadow: cs.boxShadow
            };
        }''')
        print(f"Submit button hovered:\n  textShadow: {submit_style['textShadow']}\n  boxShadow: {submit_style['boxShadow']}", flush=True)
        page.screenshot(path='scratch/submit_button_hovered_bloodred.png')
        
        # 2. Card 3D Folding Test
        print("\n--- 2. Testing 3D Card Folding In & Out ---", flush=True)
        card = page.locator('.project-card').first
        card.evaluate('el => el.scrollIntoView({ block: "center", behavior: "instant" })')
        card.hover(position={'x': 40, 'y': 40}, force=True)
        page.wait_for_timeout(250)
        
        card_folded_in = card.evaluate('''el => {
            return {
                transform: el.style.transform,
                hasFoldClass: el.classList.contains('card-folded-in'),
                boxShadow: window.getComputedStyle(el).boxShadow
            };
        }''')
        print(f"Card folded in:\n  transform: {card_folded_in['transform']}\n  hasFoldClass: {card_folded_in['hasFoldClass']}", flush=True)
        page.screenshot(path='scratch/card_folded_in_3d.png')
        
        page.mouse.move(5, 5)
        page.wait_for_timeout(500)
        card_folded_out = card.evaluate('el => el.style.transform')
        print(f"Card folded out:\n  transform: {card_folded_out}", flush=True)
        page.screenshot(path='scratch/card_folded_out_3d.png')
        page.close()
        
        # 3. Viewport Black Gap Check
        print("\n--- 3. Checking Desktop 1920px & Mobile 375px Black Gap ---", flush=True)
        for w in [1920, 1440, 768, 375]:
            p_v = browser.new_page(viewport={'width': w, 'height': 850})
            p_v.goto('http://localhost:8080/', wait_until='domcontentloaded')
            p_v.wait_for_timeout(300)
            
            gap_info = p_v.evaluate('''() => {
                const docW = document.documentElement.offsetWidth;
                const scrollW = document.documentElement.scrollWidth;
                const innerW = window.innerWidth;
                const badSections = Array.from(document.querySelectorAll('section, header, footer, main'))
                    .filter(s => s.offsetWidth > 0 && !s.closest('#birthday-mode-overlay'))
                    .filter(s => {
                        const r = s.getBoundingClientRect();
                        return Math.abs(r.right - window.innerWidth) > 2 || r.left > 2;
                    })
                    .map(s => s.id || s.className.split(' ')[0]);
                return { docW, scrollW, innerW, badSections };
            }''')
            print(f"Viewport {w}px -> docW: {gap_info['docW']}, scrollW: {gap_info['scrollW']}, badSections: {gap_info['badSections']}", flush=True)
            p_v.screenshot(path=f'scratch/viewport_verified_{w}.png')
            p_v.close()
            
        browser.close()
        print("\n--- All tests completed successfully! ---", flush=True)

if __name__ == '__main__':
    run_tests()
