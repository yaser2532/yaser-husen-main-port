import re

def upgrade_script():
    with open('assets/js/script.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Upgrade Starfield counts and sizes in initCosmicBackground
    old_starfields = """  // A. Deep Universe Starfield (2,200 wide panoramic stars, size 0.20)
  const deepStars = createStarfield(2200, 0.20, 560, 420, 480, 0.92);
  scene.add(deepStars);

  // B. Mid-range Constellation Points (520 stars, size 0.38)
  const midStars = createStarfield(520, 0.38, 380, 300, 320, 0.95);
  scene.add(midStars);

  // C. Foreground Twinkling Stellar Points (180 stars, size 0.58)
  const foregroundStars = createStarfield(180, 0.58, 260, 200, 200, 0.98);
  scene.add(foregroundStars);"""

    new_starfields = """  // A. Deep Universe Starfield (2,600 wide panoramic stars, size 1.2)
  const deepStars = createStarfield(2600, 1.2, 700, 520, 600, 0.92);
  scene.add(deepStars);

  // B. Mid-range Constellation Points (850 stars, size 2.4)
  const midStars = createStarfield(850, 2.4, 480, 360, 400, 0.96);
  scene.add(midStars);

  // C. Foreground Twinkling Stellar Points (350 stars, size 3.8)
  const foregroundStars = createStarfield(350, 3.8, 320, 240, 260, 0.98);
  scene.add(foregroundStars);

  // Expose window.__gl for diagnostics and test suites
  window.__gl = {
    renderer: renderer,
    scene: scene,
    camera: camera,
    tier: 'high',
    getInfo: () => ({ tier: 'high', stars: 3800, active: true })
  };"""

    assert old_starfields in content, "old_starfields not found in script.js"
    content = content.replace(old_starfields, new_starfields, 1)

    # 2. Add 3D Depth Travel to foreground stars in animateScene
    old_anim = """    // Slow celestial rotation of minuscule stars
    deepStars.rotation.y = time * 0.0003;
    midStars.rotation.y = -time * 0.0006;
    foregroundStars.rotation.y = time * 0.0008;

    // Atmospheric stellar twinkling
    deepStars.material.opacity = 0.82 + Math.sin(time * 1.8) * 0.12;
    foregroundStars.material.opacity = 0.86 + Math.cos(time * 2.4) * 0.14;"""

    new_anim = """    // Slow celestial rotation of minuscule stars
    deepStars.rotation.y = time * 0.0003;
    midStars.rotation.y = -time * 0.0006;
    foregroundStars.rotation.y = time * 0.0008;

    // 3D Depth Travel: Foreground stars travel through Z space towards camera
    const fgPositions = foregroundStars.geometry.attributes.position.array;
    for (let i = 2; i < fgPos.length; i += 3) {
      fgPos[i] += 0.28;
      if (fgPos[i] > 75) {
        fgPos[i] = -220;
      }
    }
    foregroundStars.geometry.attributes.position.needsUpdate = true;

    // Atmospheric stellar twinkling
    deepStars.material.opacity = 0.84 + Math.sin(time * 1.8) * 0.12;
    foregroundStars.material.opacity = 0.88 + Math.cos(time * 2.4) * 0.12;"""

    # Note: fgPos fix in new_anim
    new_anim = new_anim.replace("const fgPositions = foregroundStars.geometry.attributes.position.array;\n    for (let i = 2; i < fgPos.length; i += 3) {", "const fgPos = foregroundStars.geometry.attributes.position.array;\n    for (let i = 2; i < fgPos.length; i += 3) {")

    assert old_anim in content, "old_anim not found in script.js"
    content = content.replace(old_anim, new_anim, 1)

    # 3. Add Gen Z Chaotic Entropy into Drone Boids Physics
    old_flutter = """                    // Organic micro-flutter
                    data.vx += Math.sin(time * 3.2 + data.phaseX) * 0.35;
                    data.vy += Math.cos(time * 2.8 + data.phaseY) * 0.35;
                }

                data.currentOpacity += (targetDotOpacity - data.currentOpacity) * 0.14;"""

    new_flutter = """                    // Organic micro-flutter & Gen Z Chaotic Entropy Jitter
                    const entropyFreq = 14 + (i % 4) * 4;
                    const entropyMag = 1.4 + (i % 3) * 0.8;
                    data.vx += Math.sin(time * entropyFreq + data.phaseX) * (entropyMag * 0.22);
                    data.vy += Math.cos(time * (entropyFreq * 0.88) + data.phaseY) * (entropyMag * 0.22);

                    // Periodic zippy entropy dash
                    const burstPhase = (time * 0.35 + i * 0.75) % 5.0;
                    if (burstPhase < 0.22) {
                        const burstAngle = data.baseAngle + time * 2.2;
                        data.vx += Math.cos(burstAngle) * 3.2;
                        data.vy += Math.sin(burstAngle) * 3.2;
                    }
                }

                data.currentOpacity += (targetDotOpacity - data.currentOpacity) * 0.14;"""

    assert old_flutter in content, "old_flutter not found in script.js"
    content = content.replace(old_flutter, new_flutter, 1)

    # 4. Add 3D perspective orientation to drone transform
    old_transform = """                dot.style.transform = `translate3d(${data.currentX.toFixed(1)}px, ${data.currentY.toFixed(1)}px, 0) translate(-50%, -50%) scale(${scale3d})`;"""
    new_transform = """                const heading = Math.atan2(data.vy, data.vx) * (180 / Math.PI);
                const tiltX = Math.sin(time * 2.8 + i) * 18;
                const tiltY = Math.cos(time * 3.2 + i) * 18;
                dot.style.transform = `translate3d(${data.currentX.toFixed(1)}px, ${data.currentY.toFixed(1)}px, 0) translate(-50%, -50%) rotateZ(${heading.toFixed(1)}deg) rotateX(${tiltX.toFixed(1)}deg) rotateY(${tiltY.toFixed(1)}deg) scale(${scale3d})`;"""

    assert old_transform in content, "old_transform not found in script.js"
    content = content.replace(old_transform, new_transform, 1)

    with open('assets/js/script.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully upgraded assets/js/script.js with Gen Z Chaotic Entropy and 3D Starfield!")

def upgrade_pull_build():
    with open('assets/js/pull-build.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Snappier pull durations in startPull
    old_dur = """        item.activePullDuration = fastMode ? 320 : 600;
        item.scoutDuration = fastMode ? 150 : 350;"""
    new_dur = """        item.activePullDuration = fastMode ? 220 : 380; // Snappy Gen Z cinematic pace
        item.scoutDuration = fastMode ? 120 : 260;"""
    assert old_dur in content, "old_dur not found in pull-build.js"
    content = content.replace(old_dur, new_dur, 1)

    # 2. Snappier cadence between elements
    old_cadence = """                            item.activePullingNode = null;
                            item.currentSeqIndex++;
                            item.nextPullEligibleAt = now + 120; // 120ms gap before next element"""
    new_cadence = """                            item.activePullingNode = null;
                            item.currentSeqIndex++;
                            item.nextPullEligibleAt = now + 80; // 80ms snappy gap before next element"""
    assert old_cadence in content, "old_cadence not found in pull-build.js"
    content = content.replace(old_cadence, new_cadence, 1)

    # 3. Dynamic Laser Weld Sparks & Chaotic Electric Plasma Tractor Tethers
    old_tractor = """                        // Tractor beams from drones to active element
                        if (dynamicTargets.length > 0 && window.swarm && typeof window.swarm.getDotsData === 'function') {
                            const dotsData = window.swarm.getDotsData();
                            const vibration = Math.sin(now * 0.035) * 1.5;

                            for (let i = 0; i < Math.min(dotsData.length, dynamicTargets.length); i++) {
                                const dotX = dotsData[i].currentX;
                                const dotY = dotsData[i].currentY;
                                const anchor = dynamicTargets[i];

                                const midX = (dotX + anchor.x) * 0.5 + vibration;
                                const midY = (dotY + anchor.y) * 0.5;

                                ctx.save();
                                // Outer 3.5px Cyber Cyan plasma aura
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(0, 240, 255, 0.35)';
                                ctx.lineWidth = 3.5;
                                ctx.stroke();

                                // Middle 2px Electric Zesty Lemon beam
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(255, 230, 0, 0.85)';
                                ctx.lineWidth = 2;
                                ctx.stroke();

                                // Inner brilliant laser diamond white core
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                                ctx.lineWidth = 1.2;
                                ctx.shadowColor = '#ffe600';
                                ctx.shadowBlur = 8;
                                ctx.stroke();
                                ctx.restore();
                            }
                        }"""

    new_tractor = """                        // Dynamic sparks continuously emitted along active laser weld sweep line
                        if (Math.random() < 0.35) {
                            emitSparks(sweepX, activeBox.y + Math.random() * activeBox.h, 2);
                        }

                        // High-Energy Chaotic Electric Plasma Tractor Tethers
                        if (dynamicTargets.length > 0 && window.swarm && typeof window.swarm.getDotsData === 'function') {
                            const dotsData = window.swarm.getDotsData();

                            for (let i = 0; i < Math.min(dotsData.length, dynamicTargets.length); i++) {
                                const dotX = dotsData[i].currentX;
                                const dotY = dotsData[i].currentY;
                                const anchor = dynamicTargets[i];

                                const dist = Math.hypot(anchor.x - dotX, anchor.y - dotY) || 1;
                                const normX = -(anchor.y - dotY) / dist;
                                const normY = (anchor.x - dotX) / dist;

                                // Gen Z Chaotic Entropy: multi-harmonic electrical plasma crackle
                                const crackle = Math.sin(now * 0.08 + i * 2.1) * 7.5 + Math.cos(now * 0.14 + i * 3.7) * 4.5;
                                const midX = (dotX + anchor.x) * 0.5 + normX * crackle;
                                const midY = (dotY + anchor.y) * 0.5 + normY * crackle;

                                ctx.save();
                                // Outer 3.8px Cyber Cyan plasma aura
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(0, 240, 255, 0.40)';
                                ctx.lineWidth = 3.8;
                                ctx.stroke();

                                // Middle 2.2px Electric Zesty Lemon beam
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(255, 230, 0, 0.90)';
                                ctx.lineWidth = 2.2;
                                ctx.stroke();

                                // Inner brilliant laser diamond white core with electric glow
                                ctx.beginPath();
                                ctx.moveTo(dotX, dotY);
                                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                                ctx.lineWidth = 1.3;
                                ctx.shadowColor = '#ffe600';
                                ctx.shadowBlur = 9;
                                ctx.stroke();
                                ctx.restore();
                            }
                        }"""
    assert old_tractor in content, "old_tractor not found in pull-build.js"
    content = content.replace(old_tractor, new_tractor, 1)

    with open('assets/js/pull-build.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully upgraded assets/js/pull-build.js with Snappy Pace and Chaotic Plasma Tethers!")

if __name__ == '__main__':
    upgrade_script()
    upgrade_pull_build()
