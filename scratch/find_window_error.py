import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def find_window_error():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        await page.add_init_script("""
            window._caughtErrors = [];
            window.addEventListener('error', (e) => {
                window._caughtErrors.push({
                    message: e.message,
                    filename: e.filename,
                    lineno: e.lineno,
                    colno: e.colno,
                    error: e.error ? e.error.stack : null
                });
            });
        """)
        
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        await page.wait_for_timeout(400)
        
        errs = await page.evaluate("() => window._caughtErrors")
        print("Caught Window Errors:", errs, flush=True)
        await browser.close()

asyncio.run(find_window_error())
