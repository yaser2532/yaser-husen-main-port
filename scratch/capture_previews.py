import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.5
        )
        page = await context.new_page()

        print("1. Opening http://localhost:8080/...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Move mouse to trigger dot swarm attract-bounce hovering
        await page.mouse.move(720, 450)
        await page.wait_for_timeout(800)

        hero_path = os.path.join(ARTIFACT_DIR, "hero_preview.png")
        await page.screenshot(path=hero_path)
        print(f"Captured Hero Preview -> {hero_path}")

        # Scroll to Projects
        print("2. Scrolling to Projects section...")
        await page.evaluate("""() => {
            const el = document.getElementById('projects');
            if (el) {
                const r = el.getBoundingClientRect();
                window.scrollTo({ top: window.scrollY + r.top - 100, behavior: 'smooth' });
            }
        }""")
        await page.wait_for_timeout(1500)
        await page.mouse.move(700, 350)
        await page.wait_for_timeout(400)

        projects_path = os.path.join(ARTIFACT_DIR, "projects_preview.png")
        await page.screenshot(path=projects_path)
        print(f"Captured Projects Preview -> {projects_path}")

        # Scroll to Secret Desk & interact with lamp switch
        print("3. Scrolling to Secret Desk section...")
        await page.evaluate("""() => {
            const el = document.getElementById('secret-desk');
            if (el) {
                const r = el.getBoundingClientRect();
                window.scrollTo({ top: window.scrollY + r.top - 120, behavior: 'smooth' });
            }
        }""")
        await page.wait_for_timeout(1200)

        # Toggle lamp switch if available to show illuminated text
        try:
            lamp_toggle = page.locator("#lamp-toggle")
            if await lamp_toggle.count() > 0:
                await lamp_toggle.click()
                await page.wait_for_timeout(800)
        except Exception as e:
            print("Lamp toggle interaction note:", e)

        secret_desk_path = os.path.join(ARTIFACT_DIR, "secret_desk_preview.png")
        await page.screenshot(path=secret_desk_path)
        print(f"Captured Secret Desk Preview -> {secret_desk_path}")

        # Scroll to Footer & Nano AI Chatbot
        print("4. Scrolling to Footer and Chatbot...")
        await page.evaluate("""() => {
            window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
        }""")
        await page.wait_for_timeout(1400)

        footer_path = os.path.join(ARTIFACT_DIR, "footer_preview.png")
        await page.screenshot(path=footer_path)
        print(f"Captured Footer Preview -> {footer_path}")

        await browser.close()
        print("All previews captured successfully!")

if __name__ == "__main__":
    asyncio.run(capture())
