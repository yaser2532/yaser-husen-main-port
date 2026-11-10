import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def trace_timings():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        await page.add_init_script("""
            window._traceTimings = [];
            const origSetAttr = Element.prototype.setAttribute;
            Element.prototype.setAttribute = function(name, val) {
                if (name === 'data-drone-state') {
                    window._traceTimings.push({
                        time: performance.now(),
                        id: this.id || this.className,
                        state: val
                    });
                }
                return origSetAttr.apply(this, arguments);
            };
        """)
        
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        t_scroll = await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
            return performance.now();
        }""")
        
        await page.wait_for_timeout(3500)
        
        timings = await page.evaluate("() => window._traceTimings")
        pe_events = [t for t in timings if t['time'] >= t_scroll]
        
        for e in pe_events:
            dt = e['time'] - t_scroll
            print(f"+{dt:.1f}ms: {e['id'][:30]} -> {e['state']}", flush=True)
            
        await browser.close()

asyncio.run(trace_timings())
