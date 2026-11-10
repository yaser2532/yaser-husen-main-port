import asyncio
from playwright.async_api import async_playwright

VIEWPORTS = [
    {"name": "mobile_320", "width": 320, "height": 667},
    {"name": "mobile_375", "width": 375, "height": 812},
    {"name": "tablet_768", "width": 768, "height": 1024},
    {"name": "tablet_1024", "width": 1024, "height": 768},
    {"name": "desktop_1440", "width": 1440, "height": 900}
]

async def audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for vp in VIEWPORTS:
            page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            await page.goto("http://localhost:8080/", wait_until="networkidle")
            await asyncio.sleep(0.5)

            # Check horizontal overflow
            scroll_width, client_width = await page.evaluate("""() => [
                document.documentElement.scrollWidth,
                document.documentElement.clientWidth
            ]""")
            overflow = scroll_width > client_width
            print(f"[{vp['name']}] scrollWidth: {scroll_width}, clientWidth: {client_width}, overflow: {overflow}")

            if overflow:
                overflowing_els = await page.evaluate("""() => {
                    const docW = document.documentElement.clientWidth;
                    const bad = [];
                    document.querySelectorAll('*').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.right > docW + 2) {
                            bad.push({
                                tag: el.tagName,
                                id: el.id,
                                cls: el.className.toString().slice(0, 50),
                                right: Math.round(r.right),
                                width: Math.round(r.width)
                            });
                        }
                    });
                    return bad.slice(0, 10);
                }""")
                print(f"  Overflowing elements ({len(overflowing_els)} sample):")
                for el in overflowing_els:
                    print(f"    <{el['tag']} id='{el['id']}' class='{el['cls']}'> right={el['right']}, w={el['width']}")

            # Capture full page screenshot
            await page.screenshot(path=f"scratch/audit_{vp['name']}.png", full_page=False)
            await page.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit())
