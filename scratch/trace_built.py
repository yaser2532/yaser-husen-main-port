import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def trace_built():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        await page.add_init_script("""
            window._traceLog = [];
            const origSetAttr = Element.prototype.setAttribute;
            Element.prototype.setAttribute = function(name, val) {
                if (name === 'data-drone-state') {
                    window._traceLog.push({
                        time: performance.now(),
                        id: this.id || this.className,
                        state: val,
                        stack: (new Error().stack || '')
                    });
                }
                return origSetAttr.apply(this, arguments);
            };
        """)
        
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        print("Scrolling into view...", flush=True)
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            sec.scrollIntoView({ behavior: 'instant', block: 'start' });
        }""")
        await page.wait_for_timeout(500)
        
        log = await page.evaluate("() => window._traceLog")
        for entry in log[-15:]:
            stack_lines = entry['stack'].split('\n')
            caller = stack_lines[2].strip() if len(stack_lines) > 2 else ''
            print(f"{entry['time']:.1f}ms: {entry['id'][:30]} -> {entry['state']} (caller: {caller})", flush=True)
            
        await browser.close()

asyncio.run(trace_built())
