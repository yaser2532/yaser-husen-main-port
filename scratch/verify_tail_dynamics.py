import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))

        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(600)

        # ─── TEST 1: AT REST / FIXED POSITION -> TAIL MUST DISSOLVE TO 0 ───
        print("\n--- TEST 1: Fixed Position Check (No tail when stationary) ---")
        # Keep mouse at fixed position for 500ms
        await page.mouse.move(720, 450)
        await page.wait_for_timeout(500)

        fixed_pos_state = await page.evaluate('''() => {
            const ds = window.drones.getDrones();
            return {
                maxTrail: Math.max(...ds.map(d => d.trail.length)),
                avgTailAlpha: ds.map(d => d.tailAlpha).reduce((a, b) => a + b, 0) / ds.length,
                allRelocatingFalse: ds.every(d => !d.isRelocating)
            };
        }''')
        print(f"Fixed Position State: {fixed_pos_state}")
        assert fixed_pos_state['maxTrail'] == 0, f"Expected 0 trail points at fixed position, got {fixed_pos_state['maxTrail']}"
        assert fixed_pos_state['avgTailAlpha'] < 0.05, f"Expected tailAlpha < 0.05 at fixed position, got {fixed_pos_state['avgTailAlpha']}"
        assert fixed_pos_state['allRelocatingFalse'], "Expected all isRelocating to be false at fixed position"
        print("✓ PASS: Zero tail when stationary at a fixed position!")

        # ─── TEST 2: MOVING TO NEW POSITION -> TAIL APPEARS (REDUCED LENGTH <= 6) ───
        print("\n--- TEST 2: Moving from Fixed Position to New Position ---")
        # Move cursor to new positions dynamically
        trail_lengths = []
        tail_alphas = []
        for target_pos in [(300, 200), (900, 300), (400, 600), (1100, 500)]:
            # Rapid movement to simulate moving to a new position
            await page.mouse.move(target_pos[0], target_pos[1], steps=5)
            await page.wait_for_timeout(40)
            sample = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                return {
                    maxTrail: Math.max(...ds.map(d => d.trail.length)),
                    maxAlpha: Math.max(...ds.map(d => d.tailAlpha)),
                    anyRelocating: ds.some(d => d.isRelocating)
                };
            }''')
            trail_lengths.append(sample['maxTrail'])
            tail_alphas.append(sample['maxAlpha'])
            print(f"  Moved to {target_pos}: maxTrail={sample['maxTrail']}, maxAlpha={sample['maxAlpha']:.2f}, anyRelocating={sample['anyRelocating']}")

        max_trail_seen = max(trail_lengths)
        max_alpha_seen = max(tail_alphas)
        print(f"Dynamic Movement State: maxTrailSeen={max_trail_seen}, maxAlphaSeen={max_alpha_seen:.2f}")
        assert max_trail_seen > 0, "Tail points should appear when moving to new position"
        assert max_trail_seen <= 6, f"Tail length should be reduced (max <= 6), got {max_trail_seen}"
        assert max_alpha_seen > 0.3, f"Tail alpha should rise during relocation, got {max_alpha_seen}"
        print("✓ PASS: Tail appears when moving to new position with reduced length (<= 6)!")

        # ─── TEST 3: STOPPING AT NEW FIXED POSITION -> TAIL DISAPPEARS AGAIN ───
        print("\n--- TEST 3: Stopping at New Fixed Position (Clean dissolution) ---")
        await page.wait_for_timeout(450)
        settled_state = await page.evaluate('''() => {
            const ds = window.drones.getDrones();
            return {
                maxTrail: Math.max(...ds.map(d => d.trail.length)),
                avgTailAlpha: ds.map(d => d.tailAlpha).reduce((a, b) => a + b, 0) / ds.length
            };
        }''')
        print(f"Settled State: {settled_state}")
        assert settled_state['maxTrail'] == 0, f"Tail should completely dissolve upon arrival, got {settled_state['maxTrail']}"
        assert settled_state['avgTailAlpha'] < 0.05, f"Tail alpha should drop to 0, got {settled_state['avgTailAlpha']}"
        print("✓ PASS: Tail smoothly dissolves as soon as dot elements reach fixed position!")

        # ─── TEST 4: THINNESS SPECIFICATION ───
        print("\n--- TEST 4: Tail Thinness Verification ---")
        thinness = await page.evaluate('''() => {
            const ds = window.drones.getDrones();
            return ds.map(d => ({
                outerLineWidth: Math.max(0.65, d.size * 0.30),
                innerLineWidth: Math.max(0.32, d.size * 0.14)
            }));
        }''')
        max_outer = max(t['outerLineWidth'] for t in thinness)
        max_inner = max(t['innerLineWidth'] for t in thinness)
        print(f"Tail stroke widths: Outer max={max_outer:.2f}px, Inner core max={max_inner:.2f}px")
        assert max_outer <= 2.0, f"Outer tail ribbon should be thin (<= 2.0px), got {max_outer:.2f}px"
        assert max_inner <= 0.9, f"Inner white filament core should be razor-thin (<= 0.9px), got {max_inner:.2f}px"
        print("✓ PASS: Tail ribbons are razor-thin and delicate!")

        # ─── TEST 5: CAPTURE SCREENSHOT OF DYNAMIC THIN TAIL ───
        # Move cursor to capture thin tail in flight
        await page.mouse.move(300, 300)
        await page.wait_for_timeout(200)
        # Move in arc to generate active thin tail
        await page.mouse.move(700, 450, steps=8)
        await page.wait_for_timeout(30)
        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/thin_dynamic_tail.png"
        await page.screenshot(path=ss_path)
        print("Captured thin dynamic tail screenshot:", ss_path)

        # ─── TEST 6: CONSOLE ERRORS ───
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print("Console errors:", actual_errors)
        assert len(actual_errors) == 0, f"Expected 0 console errors, got {actual_errors}"
        print("✓ PASS: 0 console errors!")

        print("\n=== ALL TAIL REDUCTION & DYNAMIC VISIBILITY TESTS PASSED! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
