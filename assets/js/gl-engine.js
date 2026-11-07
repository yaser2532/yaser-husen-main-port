/**
 * GL-ENGINE.JS — Cyberpunk 3D WebGL Layer [PROMPT v4 / 3D-01 ... 3D-05]
 * Features:
 *   - Camera mapping 1 CSS px = 1 world unit at z = 0
 *   - 3D-01: High-Energy Hero Core (wireframe icosahedron + 30 floating crystal shards in gold/purple/turquoise)
 *   - 3D-02: Cyber Perspective Grid Backdrop + drifting cosmic dust particles
 *   - 3D-04: 8 Low-Poly 3D Drones (gold faceted body, purple glowing core, spinning turquoise fins, light cone)
 *   - 3D-05: Depth parallax on mouse move and scroll
 *   - Quality tiers & auto-downgrade (high, medium, low, off)
 *   - Window.__gl debug hook
 */

(function () {
    'use strict';

    if (typeof THREE === 'undefined') {
        console.warn('[GL-Engine] Three.js not loaded. Skipping 3D layer.');
        return;
    }

    // Check prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
        console.log('[GL-Engine] prefers-reduced-motion active. 3D layer disabled.');
        return;
    }

    // Canvas element
    let canvas = document.getElementById('gl');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'gl';
        canvas.setAttribute('aria-hidden', 'true');
        canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;';
        const body = document.body;
        body.insertBefore(canvas, body.firstChild);
    }

    let width = window.innerWidth;
    let height = window.innerHeight;
    const fov = 45;

    // Quality tier calculation
    let tier = 'high';
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (width < 768 || dpr < 1.5) {
        tier = 'medium';
    }

    // Scene & Renderer
    let renderer;
    try {
        renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: tier === 'high',
            powerPreference: 'high-performance'
        });
    } catch (e) {
        console.warn('[GL-Engine] WebGL context creation failed:', e);
        return;
    }

    renderer.setSize(width, height);
    renderer.setPixelRatio(tier === 'high' ? Math.min(dpr, 1.75) : (tier === 'medium' ? 1.25 : 1.0));
    renderer.setClearColor(0x000000, 0);

    const scene = new THREE.Scene();

    // Perspective camera where 1 world unit = 1 CSS pixel at z = 0
    const cameraZ = (height / 2) / Math.tan((fov * Math.PI / 180) / 2);
    const camera = new THREE.PerspectiveCamera(fov, width / height, 10, cameraZ * 3.5);
    camera.position.set(0, 0, cameraZ);
    camera.lookAt(0, 0, 0);

    // Color definitions [Section 2: Gold, Purple, Turquoise, Black]
    const COLOR_PURPLE = 0x9d4dff;
    const COLOR_PURPLE_DEEP = 0x3a1170;
    const COLOR_GOLD = 0xf2c14e;
    const COLOR_GOLD_BRIGHT = 0xffd873;
    const COLOR_TURQUOISE = 0x19e3d0;
    const COLOR_TURQUOISE_SOFT = 0x7ff5e8;

    // Ambient & Directional Lights
    const ambientLight = new THREE.AmbientLight(0x221133, 1.2);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(COLOR_TURQUOISE, 1.8);
    dirLight.position.set(200, 300, 400);
    scene.add(dirLight);

    const goldLight = new THREE.PointLight(COLOR_GOLD, 2.0, 1200);
    goldLight.position.set(-200, -100, 250);
    scene.add(goldLight);

    /* =========================================================================
       3D-01: HERO CORE SPHERICAL 3D MODEL REMOVED
       Wireframe icosahedron and 32 crystal shards removed per user requirement
       to optimize GPU refresh load and prevent high-memory stutter.
       ========================================================================= */
    const heroGroup = null;

    /* =========================================================================
       3D-02: CYBER PERSPECTIVE GRID BACKDROP & COSMIC DUST
       ========================================================================= */
    const backdropGroup = new THREE.Group();
    scene.add(backdropGroup);

    // Grid Floor
    const gridDim = Math.max(width * 2.4, 2800);
    const gridDivs = 40;
    const grid = new THREE.GridHelper(gridDim, gridDivs, COLOR_TURQUOISE, COLOR_PURPLE_DEEP);
    grid.position.set(0, -height * 0.65, -gridDim * 0.35);
    grid.rotation.x = 0; // horizontal floor
    grid.material.transparent = true;
    grid.material.opacity = 0.28;
    backdropGroup.add(grid);

    // ─── Rich Multi-Depth 3D Starry Night Sky & Distant Galaxy ────────────
    function createStarTexture() {
        const texCanvas = document.createElement('canvas');
        texCanvas.width = 32;
        texCanvas.height = 32;
        const c = texCanvas.getContext('2d');
        const grad = c.createRadialGradient(16, 16, 0, 16, 16, 16);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.2, 'rgba(255, 255, 255, 0.85)');
        grad.addColorStop(0.55, 'rgba(255, 255, 255, 0.30)');
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        c.fillStyle = grad;
        c.fillRect(0, 0, 32, 32);
        return new THREE.CanvasTexture(texCanvas);
    }
    const starTex = createStarTexture();

    // 1. Foreground Twinkling Stars (Vibrant, luminous, high-depth parallax)
    const FG_STARS = 450;
    const fgGeom = new THREE.BufferGeometry();
    const fgPos = new Float32Array(FG_STARS * 3);
    const fgCol = new Float32Array(FG_STARS * 3);

    const starColors = [
        new THREE.Color(0xffffff),          // Brilliant diamond white
        new THREE.Color(COLOR_GOLD_BRIGHT), // Neon Cyberpunk Gold
        new THREE.Color(COLOR_TURQUOISE),   // Neon Turquoise
        new THREE.Color(0xc084fc),          // Radiant Purple
        new THREE.Color(0x7ff5e8)           // Cyan Glow
    ];

    for (let i = 0; i < FG_STARS; i++) {
        fgPos[i * 3 + 0] = (Math.random() - 0.5) * width * 2.6;
        fgPos[i * 3 + 1] = (Math.random() - 0.5) * height * 3.2;
        fgPos[i * 3 + 2] = -Math.random() * 550 + 120;

        const c = starColors[i % starColors.length];
        fgCol[i * 3 + 0] = c.r;
        fgCol[i * 3 + 1] = c.g;
        fgCol[i * 3 + 2] = c.b;
    }

    fgGeom.setAttribute('position', new THREE.BufferAttribute(fgPos, 3));
    fgGeom.setAttribute('color', new THREE.BufferAttribute(fgCol, 3));

    const fgMat = new THREE.PointsMaterial({
        size: 3.8,
        map: starTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.95,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const fgStarfield = new THREE.Points(fgGeom, fgMat);
    backdropGroup.add(fgStarfield);

    // 2. Deep Space Background Constellations (High depth density distant galaxy)
    const BG_STARS = 1400;
    const bgGeom = new THREE.BufferGeometry();
    const bgPos = new Float32Array(BG_STARS * 3);
    const bgCol = new Float32Array(BG_STARS * 3);

    for (let i = 0; i < BG_STARS; i++) {
        bgPos[i * 3 + 0] = (Math.random() - 0.5) * width * 3.5;
        bgPos[i * 3 + 1] = (Math.random() - 0.5) * height * 4.0;
        bgPos[i * 3 + 2] = -Math.random() * 1900 - 250; // Deep Z-space

        const c = starColors[Math.floor(Math.random() * starColors.length)];
        bgCol[i * 3 + 0] = c.r * 0.95;
        bgCol[i * 3 + 1] = c.g * 0.95;
        bgCol[i * 3 + 2] = c.b * 0.95;
    }

    bgGeom.setAttribute('position', new THREE.BufferAttribute(bgPos, 3));
    bgGeom.setAttribute('color', new THREE.BufferAttribute(bgCol, 3));

    const bgMat = new THREE.PointsMaterial({
        size: 2.2,
        map: starTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.88,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const bgStarfield = new THREE.Points(bgGeom, bgMat);
    backdropGroup.add(bgStarfield);

    // 3. Cosmic Nebula Dust Cloud Layer (Soft colorful deep galaxy dust)
    const NEBULA_COUNT = 180;
    const nebGeom = new THREE.BufferGeometry();
    const nebPos = new Float32Array(NEBULA_COUNT * 3);
    const nebCol = new Float32Array(NEBULA_COUNT * 3);

    const nebColors = [
        new THREE.Color(0x9d4dff), // Violet dust
        new THREE.Color(0x19e3d0), // Turquoise dust
        new THREE.Color(0xf2c14e)  // Gold dust
    ];

    for (let i = 0; i < NEBULA_COUNT; i++) {
        nebPos[i * 3 + 0] = (Math.random() - 0.5) * width * 2.8;
        nebPos[i * 3 + 1] = (Math.random() - 0.5) * height * 3.0;
        nebPos[i * 3 + 2] = -Math.random() * 1200 - 400;

        const c = nebColors[i % nebColors.length];
        nebCol[i * 3 + 0] = c.r * 0.85;
        nebCol[i * 3 + 1] = c.g * 0.85;
        nebCol[i * 3 + 2] = c.b * 0.85;
    }

    nebGeom.setAttribute('position', new THREE.BufferAttribute(nebPos, 3));
    nebGeom.setAttribute('color', new THREE.BufferAttribute(nebCol, 3));

    const nebMat = new THREE.PointsMaterial({
        size: 9.0,
        map: starTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.42,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const nebStarfield = new THREE.Points(nebGeom, nebMat);
    backdropGroup.add(nebStarfield);

    /* =========================================================================
       3D-04: 8 LOW-POLY 3D DRONES (Gold body, purple core, spinning fins, cone)
       ========================================================================= */
    const NUM_DRONES = 8;
    const droneGroup = new THREE.Group();
    scene.add(droneGroup);

    const drones = [];

    // Shared geometries
    const droneBodyGeom = new THREE.OctahedronGeometry(9, 0); // Gold faceted body
    const droneBodyMat = new THREE.MeshPhongMaterial({
        color: COLOR_GOLD,
        emissive: 0x553d00,
        shininess: 90,
        flatShading: true
    });

    const droneCoreGeom = new THREE.SphereGeometry(4.5, 8, 8);
    const droneCoreMat = new THREE.MeshBasicMaterial({
        color: COLOR_PURPLE,
        wireframe: true
    });

    const finGeom = new THREE.BoxGeometry(16, 1.2, 3);
    const finMat = new THREE.MeshBasicMaterial({
        color: COLOR_TURQUOISE,
        transparent: true,
        opacity: 0.85
    });

    const coneGeom = new THREE.ConeGeometry(14, 38, 8, 1, true);
    const coneMat = new THREE.MeshBasicMaterial({
        color: COLOR_TURQUOISE_SOFT,
        transparent: true,
        opacity: 0.22,
        side: THREE.DoubleSide,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });

    for (let i = 0; i < NUM_DRONES; i++) {
        const drone = new THREE.Group();

        // 1. Faceted body
        const bodyMesh = new THREE.Mesh(droneBodyGeom, droneBodyMat);
        drone.add(bodyMesh);

        // 2. Purple glowing core inside
        const coreMesh = new THREE.Mesh(droneCoreGeom, droneCoreMat);
        drone.add(coreMesh);

        // 3. Spinning rotor fins
        const finMesh = new THREE.Mesh(finGeom, finMat);
        finMesh.position.y = 7;
        drone.add(finMesh);

        // 4. Downward holographic light cone
        const lightCone = new THREE.Mesh(coneGeom, coneMat);
        lightCone.position.y = -22;
        lightCone.rotation.x = Math.PI; // point downward
        drone.add(lightCone);

        drone.userData = {
            fin: finMesh,
            index: i,
            worldX: 0,
            worldY: 0,
            worldZ: 40,
            targetWorldX: 0,
            targetWorldY: 0,
            targetWorldZ: 40,
            spring: 0.12 + (i * 0.010),
            orbitAngle: (i / NUM_DRONES) * Math.PI * 2,
            orbitRadius: 70 + (i * 18) + (i % 3) * 25 // Looser, expansive orbit spacing [B-04]
        };

        droneGroup.add(drone);
        drones.push(drone);
    }

    /* =========================================================================
       INTERACTION & PARALLAX TRACKING [3D-05, H-01 ... H-06]
       ========================================================================= */
    let mouseScreenX = width * 0.5;
    let mouseScreenY = height * 0.5;
    let targetParallaxX = 0;
    let targetParallaxY = 0;
    let currentParallaxX = 0;
    let currentParallaxY = 0;
    let scrollY = window.scrollY || 0;
    let targetScrollY = scrollY;

    // Track mouse move
    window.addEventListener('mousemove', (e) => {
        mouseScreenX = e.clientX;
        mouseScreenY = e.clientY;
        
        // Normalized -1 to +1
        targetParallaxX = (e.clientX / width - 0.5) * 2;
        targetParallaxY = -(e.clientY / height - 0.5) * 2;
    }, { passive: true });

    // Track scroll
    window.addEventListener('scroll', () => {
        targetScrollY = window.scrollY || window.pageYOffset || 0;
    }, { passive: true });

    // Track resize
    window.addEventListener('resize', () => {
        width = window.innerWidth;
        height = window.innerHeight;
        renderer.setSize(width, height);
        
        const newCameraZ = (height / 2) / Math.tan((fov * Math.PI / 180) / 2);
        camera.aspect = width / height;
        camera.position.z = newCameraZ;
        camera.updateProjectionMatrix();
    });

    /* =========================================================================
       RENDER & ANIMATION LOOP
       ========================================================================= */
    let lastTime = performance.now();
    let isLoopRunning = true;
    let frameTimes = [];

    function animate(now) {
        if (!isLoopRunning) return;
        requestAnimationFrame(animate);

        const delta = Math.min((now - lastTime) * 0.001, 0.1);
        lastTime = now;

        // Auto-downgrade monitor
        if (frameTimes.length < 180) {
            frameTimes.push(delta);
        } else {
            const avgDelta = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
            if (avgDelta > 0.024 && tier === 'high') {
                tier = 'medium';
                renderer.setPixelRatio(1.25);
                console.log('[GL-Engine] Auto-downgraded to medium tier.');
            }
            frameTimes = [];
        }

        // Parallax damping
        currentParallaxX += (targetParallaxX - currentParallaxX) * 0.06;
        currentParallaxY += (targetParallaxY - currentParallaxY) * 0.06;
        scrollY += (targetScrollY - scrollY) * 0.10;

        // 1. Cyber Backdrop Perspective Drift [3D-02]
        // Grid translates forward as scroll increases (infinite highway feeling)
        grid.position.z = (-gridDim * 0.35) + ((scrollY * 0.85) % (gridDim / gridDivs));
        grid.position.x = currentParallaxX * 35;
        grid.position.y = -height * 0.65 + currentParallaxY * 20;

        // Starry Night Sky Dynamics (Twinkling & 3D Flight)
        const fgPositions = fgGeom.attributes.position.array;
        for (let i = 0; i < FG_STARS; i++) {
            // Subtle upward float + slow cosmic drift
            fgPositions[i * 3 + 1] += delta * 15;
            if (fgPositions[i * 3 + 1] > height * 1.3) {
                fgPositions[i * 3 + 1] = -height * 1.3;
            }
        }
        fgGeom.attributes.position.needsUpdate = true;

        // Twinkle pulse modulation
        fgMat.opacity = 0.80 + Math.sin(now * 0.003) * 0.18;
        bgMat.opacity = 0.65 + Math.cos(now * 0.002) * 0.15;

        // Parallax drift on star layers
        fgStarfield.position.x = currentParallaxX * 45;
        fgStarfield.position.y = currentParallaxY * 30;
        bgStarfield.position.x = currentParallaxX * 15;
        bgStarfield.position.y = currentParallaxY * 10;
        nebStarfield.position.x = currentParallaxX * 25;
        nebStarfield.position.y = currentParallaxY * 18;
        nebStarfield.rotation.y = now * 0.00015;

        // 2. 3D DRONES CHOREOGRAPHY [Phase: scout, pull, idle]
        // Coordinated with window.swarm and pull-build module
        const swarmActive = Boolean(window.swarm);
        const currentPhase = (swarmActive && typeof window.swarm.getPhase === 'function')
            ? window.swarm.getPhase()
            : (swarmActive && typeof window.swarm.isAssigned === 'function' && window.swarm.isAssigned() ? 'pull' : 'idle');
        const phaseMeta = (swarmActive && typeof window.swarm.getPhaseMeta === 'function')
            ? window.swarm.getPhaseMeta()
            : null;
        const dotsData = (swarmActive && typeof window.swarm.getDotsData === 'function')
            ? window.swarm.getDotsData()
            : null;

        const cursorWorldX = mouseScreenX - width * 0.5;
        const cursorWorldY = -(mouseScreenY - height * 0.5);

        for (let i = 0; i < NUM_DRONES; i++) {
            const drone = drones[i];
            const ud = drone.userData;

            let targetX = cursorWorldX;
            let targetY = cursorWorldY;
            let targetZ = 40;
            let rotorSpeed = 22;

            if (currentPhase === 'scout') {
                // PHASE 1: RECONNAISSANCE FORMATION
                // Dynamic 3D spiral & Lissajous sweeps across the screen & section bounds
                rotorSpeed = 46; // High-speed reconnaissance RPM
                const tScout = now * 0.0022;

                // Section target center or viewport center
                let centerX = 0;
                let centerY = 0;
                if (phaseMeta && phaseMeta.bounds) {
                    const scrollYNow = window.scrollY || window.pageYOffset || 0;
                    const bScreenY = (phaseMeta.bounds.pageTop - scrollYNow) + (phaseMeta.bounds.height * 0.4);
                    centerY = -(bScreenY - height * 0.5);
                    centerX = (phaseMeta.bounds.pageLeft + phaseMeta.bounds.width * 0.5) - width * 0.5;
                }

                // Multi-axis organic sweep: each drone has individual angle & orbital eccentricity
                const angle = tScout * (1.6 + (i % 3) * 0.5) + (i * Math.PI * 2 / NUM_DRONES);
                const rx = Math.min(width * 0.42, 260 + (i % 4) * 70);
                const ry = Math.min(height * 0.32, 160 + (i % 3) * 60);

                targetX = centerX + Math.cos(angle) * rx + Math.sin(tScout * 2.8 + i * 1.5) * 50;
                targetY = centerY + Math.sin(angle * 1.3) * ry + Math.cos(tScout * 2.1 + i) * 45;
                targetZ = 85 + Math.sin(angle * 2.2 + i) * 45;

            } else if (currentPhase === 'pull') {
                // PHASE 2: MECHANICAL ANCHOR & PULL
                // Lock onto assigned element positions from dotsData
                rotorSpeed = 34; // Deep mechanical load RPM
                if (dotsData && dotsData[i] && !isNaN(dotsData[i].currentX)) {
                    targetX = dotsData[i].currentX - width * 0.5;
                    targetY = -(dotsData[i].currentY - height * 0.5);
                    targetZ = 55 + Math.sin(now * 0.005 + i) * 12;
                } else {
                    targetX = cursorWorldX;
                    targetY = cursorWorldY;
                    targetZ = 45;
                }

            } else {
                // PHASE 3: IDLE FLUID ORBIT AROUND CURSOR / TOUCH (Loose, airy escort cloud)
                rotorSpeed = 20;
                const orbitSpeed = 0.95 + (i % 3) * 0.3;
                const angle = ud.orbitAngle + now * 0.0012 * orbitSpeed;
                const ox = Math.cos(angle) * ud.orbitRadius + Math.sin(now * 0.0016 + i) * 35;
                const oy = Math.sin(angle * 1.25) * (ud.orbitRadius * 0.65) + Math.cos(now * 0.0014 + i) * 28;
                targetX = cursorWorldX + ox;
                targetY = cursorWorldY + oy;
                targetZ = 45 + Math.sin(angle * 1.8 + i) * 22;
            }

            // Spin rotor fin
            ud.fin.rotation.y += delta * rotorSpeed;

            // Smooth spring lerp
            const lerpFactor = (currentPhase === 'scout') ? 0.085 : ud.spring;
            ud.worldX += (targetX - ud.worldX) * lerpFactor;
            ud.worldY += (targetY - ud.worldY) * lerpFactor;
            ud.worldZ += (targetZ - ud.worldZ) * 0.12;

            drone.position.set(ud.worldX, ud.worldY, ud.worldZ);

            // Aerodynamic banking: realistic roll and pitch based on velocity vector
            const vx = (targetX - ud.worldX) * 0.025;
            const vy = (targetY - ud.worldY) * 0.025;
            const targetRoll = -Math.max(-0.65, Math.min(0.65, vx));
            const targetPitch = Math.max(-0.55, Math.min(0.55, vy));
            drone.rotation.z += (targetRoll - drone.rotation.z) * 0.18;
            drone.rotation.x += (targetPitch - drone.rotation.x) * 0.18;
            drone.rotation.y = Math.sin(now * 0.0025 + i) * 0.25;
        }

        // Render Scene
        renderer.render(scene, camera);
    }

    // Start render loop
    requestAnimationFrame(animate);

    // Sleep when tab hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isLoopRunning = false;
        } else {
            if (!isLoopRunning) {
                isLoopRunning = true;
                lastTime = performance.now();
                requestAnimationFrame(animate);
            }
        }
    });

    // Expose window.__gl for verification & diagnostics
    window.__gl = {
        renderer: renderer,
        scene: scene,
        camera: camera,
        heroGroup: heroGroup,
        drones: drones,
        get tier() { return tier; },
        getInfo: function () {
            return {
                renderCalls: renderer.info.render.calls,
                triangles: renderer.info.render.triangles,
                frame: renderer.info.render.frame,
                tier: tier
            };
        }
    };

    console.log('[GL-Engine] Cyberpunk 3D WebGL Layer initialized successfully. Tier:', tier);
})();
