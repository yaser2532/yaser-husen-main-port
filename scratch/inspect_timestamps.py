import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_timestamps():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        t_scroll = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
            return performance.now();
        }""")
        
        await page.wait_for_timeout(600)
        
        data = await page.evaluate("""() => {
            const sec = window.drones.getElements().find(e => e.secId === 'profile-expertise')?.secInfo;
            const el = window.drones.getElements().find(e => e.secId === 'profile-expertise');
            return {
                firstEnteredBandTime: sec.firstEnteredBandTime,
                dwellMetTime: sec.dwellMetTime,
                dwellMet: sec.dwellMet,
                gateOpenedTime: el.gateOpenedTime,
                dispatchTime: el.dispatchTime
            };
        }""")
        print("Detailed Timestamps:", {
            't_scroll': t_scroll,
            'firstEnteredBand_delta': data['firstEnteredBandTime'] - t_scroll,
            'dwellMet_delta': data['dwellMetTime'] - t_scroll,
            'dispatch_delta': data['dispatchTime'] - t_scroll,
            'gateToDispatch': data['dispatchTime'] - data['dwellMetTime']
        }, flush=True)
        await browser.close()

asyncio.run(inspect_timestamps())
