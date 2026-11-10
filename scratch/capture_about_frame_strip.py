import asyncio
import sys
import os
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def capture_strip():
    os.makedirs('scratch/frame_strip', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        print("Scrolling to about-me section...", flush=True)
        await page.evaluate("""() => {
            const sec = document.getElementById('about-me');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 60, behavior: 'instant' });
        }""")
        
        # Capture sequence of 6 beats:
        # 1: Hive Pulse (0-110ms)
        await page.wait_for_timeout(100)
        await page.screenshot(path='scratch/frame_strip/beat1_hive_pulse.png')
        print("Captured Beat 1: Hive pulse", flush=True)
        
        # 2: Stream Flight (110-430ms)
        await page.wait_for_timeout(180)
        await page.screenshot(path='scratch/frame_strip/beat2_stream_flight.png')
        print("Captured Beat 2: Stream ribbon flight", flush=True)
        
        # 3: Lock-on HUD brackets & Tractor Beams (430-550ms)
        await page.wait_for_timeout(200)
        await page.screenshot(path='scratch/frame_strip/beat3_lock_on.png')
        print("Captured Beat 3: Lock-on HUD brackets & Beams", flush=True)
        
        # 4: Pull Assembly (code IDE & paragraphs)
        await page.wait_for_timeout(350)
        await page.screenshot(path='scratch/frame_strip/beat4_pull_assembly.png')
        print("Captured Beat 4: Pull assembly", flush=True)
        
        # 5: Impact RGB Flash
        await page.wait_for_timeout(300)
        await page.screenshot(path='scratch/frame_strip/beat5_impact_flash.png')
        print("Captured Beat 5: Impact flash", flush=True)
        
        # 6: Release & Spiral Return
        await page.wait_for_timeout(350)
        await page.screenshot(path='scratch/frame_strip/beat6_release_return.png')
        print("Captured Beat 6: Release & Return", flush=True)
        
        await browser.close()
    print("Frame strip completed successfully!", flush=True)

asyncio.run(capture_strip())
