import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)

        # Scroll to about-me
        await page.evaluate("document.getElementById('about-me').scrollIntoView()")
        await page.wait_for_timeout(1000)

        info = await page.evaluate('''() => {
            const cb = document.querySelector('.code-block-visual');
            const lines = Array.from(cb.querySelectorAll('.drone-code-line'));
            return {
                cbExists: !!cb,
                cbDroneState: cb.getAttribute('data-drone-state'),
                cbDisplay: window.getComputedStyle(cb).display,
                cbOpacity: window.getComputedStyle(cb).opacity,
                cbVisibility: window.getComputedStyle(cb).visibility,
                cbRect: cb.getBoundingClientRect(),
                parentRect: cb.parentElement.getBoundingClientRect(),
                lineCount: lines.length,
                linesInfo: lines.map(l => ({
                    text: l.innerText,
                    clipPath: window.getComputedStyle(l).clipPath,
                    opacity: window.getComputedStyle(l).opacity,
                    revealed: l.classList.contains('revealed')
                }))
            };
        }''')
        print("CODE BLOCK VISUAL INFO:")
        print(f"Exists: {info['cbExists']}, DroneState: {info['cbDroneState']}, Opacity: {info['cbOpacity']}")
        print(f"Rect: {info['cbRect']}")
        print(f"Line Count: {info['lineCount']}")
        for idx, l in enumerate(info['linesInfo']):
            print(f"  Line {idx}: revealed={l['revealed']}, clipPath={l['clipPath']}, text={repr(l['text'])}")

        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/inspect_code_block.png"
        await page.screenshot(path=ss_path)
        print("Screenshot saved to:", ss_path)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
