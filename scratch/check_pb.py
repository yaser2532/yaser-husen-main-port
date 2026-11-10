import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="msedge", headless=True)
        page = await b.new_page()
        with open("assets/js/pull-build.js", "r", encoding="utf-8") as f:
            code = f.read()

        res = await page.evaluate("""(src) => {
            const lines = src.split('\\n');
            let depth = 0;
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                for (let ch of line) {
                    if (ch === '{') depth++;
                    if (ch === '}') {
                        depth--;
                        if (depth < 0) {
                            return { lineNum: i + 1, line, depth, reason: 'Negative depth (unmatched closing brace)' };
                        }
                    }
                }
            }
            return { totalLines: lines.length, finalDepth: depth };
        }""", code)
        print("Brace depth result:", res)
        await b.close()

if __name__ == "__main__":
    asyncio.run(test())
