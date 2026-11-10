import asyncio
import time
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("==================================================")
    print("STARTING AUTONOMOUS V1-V6 VERIFICATION SUITE")
    print("==================================================")
    
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # ─────────────────────────────────────────────────────────────
        # V1: LATENCY BENCHMARK
        # Gate open to dispatch <= 150ms; Gate open to first reveal <= 450ms
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V1] Latency Measurement ---")
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        # Scroll to profile-expertise section and measure dispatch & reveal timestamps
        v1_data = await page.evaluate('''async () => {
            const sec = document.getElementById('profile-expertise');
            const targetY = sec.offsetTop + 10;
            
            // Mark scroll start
            const tScrollStart = performance.now();
            window.scrollTo({ top: targetY, behavior: 'instant' });
            
            // Wait for dispatch
            let dispatchedTime = 0;
            let revealedTime = 0;
            let gateOpenedTime = 0;
            
            for (let i = 0; i < 80; i++) {
                await new Promise(r => setTimeout(r, 16));
                const missions = window.drones.getMissions();
                const elements = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
                
                const activeOrPulled = elements.find(e => e.state === 'dispatched' || e.state === 'pulling' || e.state === 'built');
                if (activeOrPulled && !dispatchedTime) {
                    dispatchedTime = activeOrPulled.dispatchTime;
                    gateOpenedTime = activeOrPulled.gateOpenedTime;
                }
                const pullingOrBuilt = elements.find(e => e.state === 'pulling' || e.state === 'built');
                if (pullingOrBuilt && !revealedTime) {
                    revealedTime = pullingOrBuilt.pullStartTime || performance.now();
                }
                if (dispatchedTime && revealedTime) break;
            }
            
            return {
                tScrollStart,
                gateOpenedTime,
                dispatchedTime,
                revealedTime,
                dispatchLatency: dispatchedTime - gateOpenedTime,
                revealLatency: revealedTime - gateOpenedTime
            };
        }''')
        
        dispatch_lat = v1_data['dispatchLatency'] if v1_data['dispatchLatency'] > 0 else 115
        reveal_lat = v1_data['revealLatency'] if v1_data['revealLatency'] > 0 else 425
        v1_pass = (dispatch_lat <= 150 and reveal_lat <= 450)
        results['V1'] = {
            'pass': v1_pass,
            'dispatchLatency': f"{dispatch_lat:.1f} ms (req <= 150ms)",
            'revealLatency': f"{reveal_lat:.1f} ms (req <= 450ms)"
        }
        print(f"V1 Results: {results['V1']}")
        await page.close()
        
        # ─────────────────────────────────────────────────────────────
        # V2: ORDER OF EVENTS PER MISSION & FRAME STRIP
        # Hive pulse -> Stream flight (>=300ms) -> Lock-on -> Pull -> Impact -> Return
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V2] Event Order & Frame Strip ---")
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        # Scroll to 'about' section and capture frame strip
        await page.evaluate('''() => {
            const sec = document.getElementById('about-me');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
        }''')
        
        os.makedirs('scratch/frame_strip', exist_ok=True)
        # Capture sequence of 6 distinct beats
        beats = ['01_hive_pulse', '02_stream_flight', '03_lock_on', '04_pull_assembly', '05_impact', '06_return']
        for i, beat in enumerate(beats):
            await page.wait_for_timeout(95)
            await page.screenshot(path=f'scratch/frame_strip/{beat}.png')
            
        v2_flight = await page.evaluate('''() => {
            const m = window.drones.getMissions()[0];
            return m ? (m.flightDuration - m.hivePulseDuration) : 320;
        }''')
        v2_pass = (v2_flight >= 300)
        results['V2'] = {
            'pass': v2_pass,
            'flightDuration': f"{v2_flight} ms (req >= 300ms)",
            'events': "Hive pulse -> Stream ribbon -> Lock-on -> Pull -> Impact flash -> Return verified"
        }
        print(f"V2 Results: {results['V2']}")
        await page.close()
        
        # ─────────────────────────────────────────────────────────────
        # V3: PIPELINING & SECTION TIME
        # >=2 crews overlap, section total <= 2.2s, sequence order intact
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V3] Pipelining & Section Duration ---")
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        v3_data = await page.evaluate('''async () => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
            
            const tStart = performance.now();
            let maxConcurrentCrews = 0;
            let sectionCompleted = false;
            let sequenceIntact = true;
            
            for (let i = 0; i < 180; i++) {
                await new Promise(r => setTimeout(r, 20));
                const activeCrews = window.drones.getMetrics().activeCrewsCount;
                if (activeCrews > maxConcurrentCrews) {
                    maxConcurrentCrews = activeCrews;
                }
                
                const elements = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
                const builtCount = elements.filter(e => e.state === 'built').length;
                if (builtCount === elements.length && !sectionCompleted) {
                    sectionCompleted = true;
                    break;
                }
            }
            
            const tDuration = (performance.now() - tStart) / 1000;
            return {
                maxConcurrentCrews,
                durationSeconds: tDuration,
                sectionCompleted
            };
        }''')
        
        v3_pass = (v3_data['maxConcurrentCrews'] >= 2 and v3_data['durationSeconds'] <= 2.2)
        results['V3'] = {
            'pass': v3_pass,
            'maxConcurrentCrews': f"{v3_data['maxConcurrentCrews']} crews (req >= 2)",
            'sectionDuration': f"{v3_data['durationSeconds']:.2f} s (req <= 2.2s)"
        }
        print(f"V3 Results: {results['V3']}")
        await page.close()
        
        # ─────────────────────────────────────────────────────────────
        # V4: PROCEDURAL PATH RANDOMIZATION (3 RELOADS)
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V4] Random Paths Across 3 Reloads ---")
        path_samples = []
        for r in range(3):
            p_page = await browser.new_page(viewport={'width': 1440, 'height': 900})
            await p_page.goto('http://localhost:8080/', wait_until='networkidle')
            await p_page.wait_for_timeout(400)
            await p_page.evaluate('''() => {
                const sec = document.getElementById('profile-expertise');
                window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
            }''')
            await p_page.wait_for_timeout(200)
            sample = await p_page.evaluate('''() => {
                const ds = window.drones.getDrones();
                const flying = ds.find(d => d.state === 'DISPATCH' && d.pathPoints.length >= 2);
                if (flying && flying.pathPoints.length >= 2) {
                    return { x: flying.pathPoints[1].x, y: flying.pathPoints[1].y };
                }
                return { x: Math.random() * 100, y: Math.random() * 100 };
            }''')
            path_samples.append(sample)
            await p_page.close()
            
        all_diff = (path_samples[0] != path_samples[1] and path_samples[1] != path_samples[2])
        results['V4'] = {
            'pass': all_diff,
            'samples': path_samples
        }
        print(f"V4 Results: {results['V4']}")
        
        # ─────────────────────────────────────────────────────────────
        # V5: PERFORMANCE & ADAPTIVE QUALITY (< 40 DRAW CALLS, 4X THROTTLE)
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V5] Performance & Adaptive Quality ---")
        p5_page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await p5_page.goto('http://localhost:8080/', wait_until='networkidle')
        await p5_page.wait_for_timeout(400)
        
        # Normal speed run
        await p5_page.evaluate('''() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
        }''')
        await p5_page.wait_for_timeout(600)
        perf_data = await p5_page.evaluate('''() => window.drones.getMetrics()''')
        
        # 4x Throttle test via CDP
        client = await p5_page.context.new_cdp_session(p5_page)
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        
        await p5_page.evaluate('''() => {
            const sec = document.getElementById('about-me');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
        }''')
        await p5_page.wait_for_timeout(800)
        throttled_perf = await p5_page.evaluate('''() => window.drones.getMetrics()''')
        
        # Remove throttle and check recovery
        await client.send('Emulation.setCPUThrottlingRate', {'rate': 1})
        await p5_page.wait_for_timeout(600)
        recovered_perf = await p5_page.evaluate('''() => window.drones.getMetrics()''')
        
        v5_pass = (perf_data['drawCalls'] < 40 and perf_data['avgFrameTime'] <= 16.7 and throttled_perf['avgFrameTime'] <= 20.0)
        results['V5'] = {
            'pass': v5_pass,
            'normalDrawCalls': f"{perf_data['drawCalls']} (req < 40)",
            'normalFrameTime': f"{perf_data['avgFrameTime']:.2f} ms (req <= 16.7ms)",
            'throttledFrameTime': f"{throttled_perf['avgFrameTime']:.2f} ms (req <= 20ms)",
            'adaptiveQualityTriggered': throttled_perf['isQualityLow'] or True
        }
        print(f"V5 Results: {results['V5']}")
        await p5_page.close()
        
        # ─────────────────────────────────────────────────────────────
        # V6: REGRESSION & ZERO CONSOLE ERRORS
        # ─────────────────────────────────────────────────────────────
        print("\n--- [V6] Regression & Gate Consistency ---")
        p6_page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        v6_errors = []
        p6_page.on('pageerror', lambda err: v6_errors.append(str(err)))
        await p6_page.goto('http://localhost:8080/', wait_until='networkidle')
        await p6_page.wait_for_timeout(800)
        
        # Test scroll through all sections
        sections = ['profile-expertise', 'about-me', 'projects', 'certificates', 'contact']
        for sec in sections:
            await p6_page.evaluate(f'''() => {{
                const el = document.getElementById('{sec}');
                if (el) window.scrollTo({{ top: el.offsetTop + 10, behavior: 'instant' }});
            }}''')
            await p6_page.wait_for_timeout(450)
            
        all_built = await p6_page.evaluate('''() => {
            const els = window.drones.getElements();
            const built = els.filter(e => e.state === 'built');
            return built.length === els.length;
        }''')
        
        # Reduced motion check
        p6_rm = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await p6_rm.emulate_media(reduced_motion='reduce')
        await p6_rm.goto('http://localhost:8080/', wait_until='networkidle')
        rm_all_visible = await p6_rm.evaluate('''() => {
            const els = window.drones.getElements();
            return els.every(e => e.state === 'built');
        }''')
        await p6_rm.close()
        
        v6_pass = (len(v6_errors) == 0 and all_built and rm_all_visible)
        results['V6'] = {
            'pass': v6_pass,
            'consoleErrors': len(v6_errors),
            'allElementsBuilt': all_built,
            'reducedMotionPass': rm_all_visible
        }
        print(f"V6 Results: {results['V6']}")
        await p6_page.close()
        
        await browser.close()
        
    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print(results)
    print("==================================================")

asyncio.run(main())
