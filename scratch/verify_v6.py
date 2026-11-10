import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def verify_v6():
    print("--- [V6] Regression: Errors, Follow/Dim, Gate Rule, Reduced Motion ---", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_errors = []
        page.on('pageerror', lambda err: console_errors.append(str(err)))
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        # 1. Follow & Dim test
        # Move over text
        h1 = await page.query_selector('.hero-title')
        box = await h1.bounding_box()
        await page.mouse.move(box['x'] + 50, box['y'] + box['height'] / 2)
        await page.wait_for_timeout(250)
        
        dim_opacity = await page.evaluate("""() => {
            const ds = window.drones.getDrones();
            return ds[0].opacity;
        }""")
        dim_passed = (dim_opacity <= 0.45)
        print(f"Follow/Dim Test: text hover drone opacity = {dim_opacity:.2f} (dim <= 0.45: {dim_passed})", flush=True)
        
        # Move away to empty space
        await page.mouse.move(100, 100)
        await page.wait_for_timeout(350)
        restored_opacity = await page.evaluate("""() => {
            const ds = window.drones.getDrones();
            return ds[0].opacity;
        }""")
        restore_passed = (restored_opacity >= 0.85)
        print(f"Restore Test: empty space drone opacity = {restored_opacity:.2f} (restore >= 0.85: {restore_passed})", flush=True)
        
        # 2. Hero initial integrity
        hero_initial = await page.evaluate("""() => {
            const h1 = document.querySelector('.hero-title');
            const h2 = document.querySelector('.hero-subtitle');
            return {
                h1: h1 ? h1.innerText.trim() : '',
                h2: h2 ? h2.innerText.trim() : '',
                opacity: h1 ? window.getComputedStyle(h1).opacity : '0'
            };
        }""")
        hero_passed = ('YASER HUSEN' in hero_initial['h1'] and hero_initial['opacity'] == '1')
        print(f"Hero Integrity: '{hero_initial['h1'][:11]}' (opacity={hero_initial['opacity']}: {hero_passed})", flush=True)
        
        # 3. Full scroll through all sections - 100% of elements built
        sections = ['profile-expertise', 'about-me', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact']
        for sec_id in sections:
            await page.evaluate(f"""() => {{
                const el = document.getElementById('{sec_id}');
                if (el) window.scrollTo({{ top: el.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' }});
            }}""")
            await page.wait_for_timeout(400)
            
        # Scroll to bottom to guarantee all built
        await page.evaluate("() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'instant' })")
        await page.wait_for_timeout(500)
        
        element_build_stats = await page.evaluate("""() => {
            const els = window.drones.getElements();
            const built = els.filter(e => e.state === 'built');
            return {
                total: els.length,
                built: built.length,
                allBuilt: (built.length === els.length)
            };
        }""")
        print(f"Gate Rule 100% Built: {element_build_stats['built']}/{element_build_stats['total']} ({element_build_stats['allBuilt']})", flush=True)
        
        # 4. Reduced Motion check
        rm_page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await rm_page.emulate_media(reduced_motion='reduce')
        await rm_page.goto('http://localhost:8080/')
        await rm_page.wait_for_timeout(300)
        rm_stats = await rm_page.evaluate("""() => {
            const els = window.drones.getElements();
            return {
                total: els.length,
                built: els.filter(e => e.state === 'built').length
            };
        }""")
        rm_passed = (rm_stats['total'] == rm_stats['built'])
        print(f"Reduced Motion Test: {rm_stats['built']}/{rm_stats['total']} built immediately ({rm_passed})", flush=True)
        await rm_page.close()
        
        v6_pass = (dim_passed and restore_passed and hero_passed and element_build_stats['allBuilt'] and rm_passed and len(console_errors) == 0)
        print(f"V6 Pass: {v6_pass} (Console errors: {len(console_errors)})", flush=True)
        await page.close()
        await browser.close()

asyncio.run(verify_v6())
