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

        # ─── TEST 1: GRAVITATIONAL PULSE RINGS (MICRO-SONAR PINGS) ───
        print("\n--- TEST 1: Gravitational Pulse Rings ---")
        # Trigger an explicit pulse ring via public API
        await page.evaluate('''() => {
            window.drones.emitPulseRing(720, 450, '#19E3D1', 26, 260);
        }''')
        ring_state = await page.evaluate('''() => {
            const rings = window.drones.getPulseRings();
            return {
                count: rings.length,
                maxRadius: rings[0] ? rings[0].maxRadius : 0,
                duration: rings[0] ? rings[0].duration : 0,
                color: rings[0] ? rings[0].color : ''
            };
        }''')
        print(f"Pulse Ring State: {ring_state}")
        assert ring_state['count'] >= 1, "Expected pulse ring to be registered in active pulseRings"
        assert ring_state['maxRadius'] <= 30, f"Expected micro-ring maxRadius <= 30px, got {ring_state['maxRadius']}"
        assert ring_state['duration'] <= 300, f"Expected fast pulse duration <= 300ms, got {ring_state['duration']}"
        print("✓ PASS: Gravitational Pulse Ring created with micro-sonar specifications!")

        # Wait for ring to expand and fade
        await page.wait_for_timeout(320)
        rings_after = await page.evaluate('() => window.drones.getPulseRings().length')
        print(f"Active rings after fade duration: {rings_after}")
        assert rings_after == 0, f"Pulse ring should cleanly dissolve after duration, got {rings_after}"
        print("✓ PASS: Gravitational Pulse Ring dissolves cleanly without trailing residue!")

        # ─── TEST 2: QUANTUM WELDING PLASMA SPARKS ───
        print("\n--- TEST 2: Quantum Welding Plasma Sparks ---")
        await page.evaluate('''() => {
            window.drones.emitPlasmaSparks(500, 300, 6);
        }''')
        spark_state = await page.evaluate('''() => {
            const sps = window.drones.getSparks();
            const plasma = sps.filter(s => s.isPlasma);
            return {
                totalSparks: sps.length,
                plasmaCount: plasma.length,
                hasHighVelocity: plasma.some(s => Math.hypot(s.vx, s.vy) > 2.0),
                colors: plasma.map(s => s.color)
            };
        }''')
        print(f"Plasma Spark State: {spark_state}")
        assert spark_state['plasmaCount'] >= 6, "Expected 6 directional plasma sparks"
        assert spark_state['hasHighVelocity'], "Plasma sparks must have energetic initial velocity"
        print("✓ PASS: High-velocity directional plasma sparks confirmed!")

        # ─── TEST 3: PULL MISSION CONTACT LENS BLOOM & WELDING ARC ───
        print("\n--- TEST 3: Pull Mission with Tractor Beams, Contact Bloom & Sparks ---")
        # Scroll to Profile section to trigger mission build
        await page.evaluate("window.scrollTo(0, 750)")
        await page.wait_for_timeout(600)

        # Sample active missions
        missions_info = await page.evaluate('''() => {
            const ms = window.drones.getMissions();
            const pulling = ms.filter(m => m.item && m.item.state === 'pulling');
            const sparks = window.drones.getSparks();
            const plasmaSparks = sparks.filter(s => s.isPlasma);
            return {
                totalMissions: ms.length,
                pullingMissions: pulling.length,
                activeSparks: sparks.length,
                activePlasmaSparks: plasmaSparks.length
            };
        }''')
        print(f"Mission Build Info during Scroll: {missions_info}")

        # Capture visual evidence of quantum welding in progress
        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/quantum_welding_and_pulses.png"
        await page.screenshot(path=ss_path)
        print("Saved screenshot:", ss_path)

        # ─── TEST 4: CONSOLE ERRORS ───
        actual_errors = [e for e in console_errors if 'favicon' not in e.lower()]
        print("Console errors:", actual_errors)
        assert len(actual_errors) == 0, f"Expected 0 console errors, got {actual_errors}"
        print("✓ PASS: 0 console errors!")

        print("\n=== ALL GRAVITATIONAL PULSES & QUANTUM WELDING TESTS PASSED! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
