import asyncio
from playwright.async_api import async_playwright

async def audit_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for width, name in [(375, "mobile_375"), (768, "tablet_768")]:
            page = await browser.new_page(viewport={"width": width, "height": 812})
            await page.goto("http://localhost:8080/", wait_until="networkidle")
            await asyncio.sleep(0.5)

            # Scroll down in increments of 500px to document bottom
            max_scroll = await page.evaluate("document.documentElement.scrollHeight")
            print(f"\n--- Checking {name} (height: {max_scroll}px) ---")
            
            overflow_found = False
            for y in range(0, max_scroll, 600):
                await page.evaluate(f"window.scrollTo(0, {y})")
                await asyncio.sleep(0.08)
                sw, cw = await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                if sw > cw:
                    overflow_found = True
                    bad = await page.evaluate("""() => {
                        const cw = document.documentElement.clientWidth;
                        const list = [];
                        document.querySelectorAll('*').forEach(el => {
                            const r = el.getBoundingClientRect();
                            if (r.right > cw + 1 && r.width > 0) {
                                list.push({
                                    tag: el.tagName,
                                    id: el.id,
                                    cls: el.className.toString().slice(0, 40),
                                    right: Math.round(r.right),
                                    width: Math.round(r.width)
                                });
                            }
                        });
                        return list.slice(0, 5);
                    }""")
                    print(f"  Overflow at y={y}: scrollWidth={sw} > clientWidth={cw}")
                    for b in bad:
                        print(f"    <{b['tag']} id='{b['id']}' class='{b['cls']}'> right={b['right']}, w={b['width']}")
                    break

            if not overflow_found:
                print(f"  [PASS] No horizontal overflow detected during scroll in {name}!")

            await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit_scroll())
