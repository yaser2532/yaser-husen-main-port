import asyncio
import json
from playwright.async_api import async_playwright

async def profile():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile emulation (Pixel 5 or iPhone)
        context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            user_agent='Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True
        )
        page = await context.new_page()
        
        # Emulate 4x CPU throttling via Chrome DevTools Protocol
        client = await context.new_cdp_session(page)
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        
        print("Starting performance measurement on http://localhost:8080/ ...")
        t0 = asyncio.get_event_loop().time()
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        load_time = (asyncio.get_event_loop().time() - t0) * 1000
        
        # Evaluate web vitals and DOM metrics
        metrics = await page.evaluate('''() => {
            const perf = window.performance;
            const timing = perf.timing;
            const paintEntries = perf.getEntriesByType('paint');
            const fcp = paintEntries.find(e => e.name === 'first-contentful-paint');
            
            // Check scripts in head/body
            const scripts = Array.from(document.querySelectorAll('script')).map(s => ({
                src: s.src,
                async: s.async,
                defer: s.defer,
                type: s.type
            }));
            
            // Check images
            const images = Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src,
                loading: img.loading,
                width: img.width,
                height: img.height,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight
            }));
            
            // Check stylesheets & fonts
            const stylesheets = Array.from(document.querySelectorAll('link[rel=\"stylesheet\"]')).map(l => l.href);
            
            return {
                fcp: fcp ? fcp.startTime : null,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                load: timing.loadEventEnd - timing.navigationStart,
                scriptsCount: scripts.length,
                scripts,
                imagesCount: images.length,
                images: images.slice(0, 8),
                stylesheets
            };
        }''')
        
        print(f"DOMContentLoaded: {metrics['domContentLoaded']} ms")
        print(f"Load Event: {metrics['load']} ms")
        print(f"FCP: {metrics['fcp']} ms")
        print(f"Scripts: {metrics['scriptsCount']}")
        for s in metrics['scripts']:
            print(f"  script: {s['src'].split('/')[-1] if s['src'] else 'inline'} (defer={s['defer']}, async={s['async']})")
        print(f"Images: {metrics['imagesCount']}")
        for img in metrics['images']:
            print(f"  img: {img['src'].split('/')[-1]} (loading={img['loading']}, w={img['width']}, h={img['height']})")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(profile())
