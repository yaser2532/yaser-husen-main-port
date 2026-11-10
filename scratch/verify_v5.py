import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def verify_v5():
    print("--- [V5] Testing Performance & 4x Throttle ---", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        # 1. Normal performance during build mission
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        
        frame_times = []
        draw_calls = []
        for _ in range(30):
            await page.wait_for_timeout(20)
            m = await page.evaluate("() => window.drones.getMetrics()")
            frame_times.append(m['avgFrameTime'])
            draw_calls.append(m['drawCalls'])
            
        normal_avg_frame = sum(frame_times) / len(frame_times)
        max_draw_call = max(draw_calls)
        print(f"Normal Perf: avgFrameTime={normal_avg_frame:.2f}ms, maxDrawCalls={max_draw_call}", flush=True)
        
        # 2. 4x CPU Throttle test
        client = await page.context.new_cdp_session(page)
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        
        # Scroll to about-me to trigger mission under throttle
        await page.evaluate("""() => {
            const sec = document.getElementById('about-me');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        
        throttled_frames = []
        for _ in range(40):
            await page.wait_for_timeout(20)
            m = await page.evaluate("() => window.drones.getMetrics()")
            throttled_frames.append(m['avgFrameTime'])
            
        throttled_avg_frame = sum(throttled_frames) / len(throttled_frames)
        quality_low_triggered = await page.evaluate("() => window.drones.getMetrics().isQualityLow")
        print(f"4x Throttled Perf: avgFrameTime={throttled_avg_frame:.2f}ms, qualityLow={quality_low_triggered}", flush=True)
        
        # 3. Recovery test
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 1})
        await page.wait_for_timeout(600)
        recovered_metrics = await page.evaluate("() => window.drones.getMetrics()")
        print(f"Recovered Perf: avgFrameTime={recovered_metrics['avgFrameTime']:.2f}ms, qualityLow={recovered_metrics['isQualityLow']}", flush=True)
        
        v5_pass = (normal_avg_frame <= 16.7 and throttled_avg_frame <= 20.0 and max_draw_call < 40)
        print(f"V5 Pass: {v5_pass} (Normal Frame: {normal_avg_frame:.2f}ms <= 16.7ms, Throttled Frame: {throttled_avg_frame:.2f}ms <= 20ms, Draw Calls: {max_draw_call} < 40)", flush=True)
        await browser.close()

asyncio.run(verify_v5())
