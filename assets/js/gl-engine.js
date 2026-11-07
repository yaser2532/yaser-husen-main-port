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
       3D-01: HERO CORE (Wireframe Icosahedron + 30 Floating Crystal Shards)
       ========================================================================= */
    const heroGroup = new THREE.Group();
    scene.add(heroGroup);

    // Base radius scales with viewport
    const heroRadius = Math.min(width * 0.16, 170);
    
    // Outer wireframe icosahedron
    const icoGeom = new THREE.IcosahedronGeometry(heroRadius, 1);
    const wireGeom = new THREE.WireframeGeometry(icoGeom);
    const wireMat = new THREE.LineBasicMaterial({
        color: COLOR_PURPLE,
        transparent: true,
        opacity: 0.65,
        linewidth: 1
    });
    const wireMesh = new THREE.LineSegments(wireGeom, wireMat);
    heroGroup.add(wireMesh);

    // Inner glowing faceted icosahedron
    const innerIcoGeom = new THREE.IcosahedronGeometry(heroRadius * 0.72, 0);
    const innerIcoMat = new THREE.MeshPhongMaterial({
        color: COLOR_PURPLE_DEEP,
        emissive: 0x4a1885,
        wireframe: false,
        shininess: 90,
        transparent: true,
        opacity: 0.82
    });
    const innerIcoMesh = new THREE.Mesh(innerIcoGeom, innerIcoMat);
    heroGroup.add(innerIcoMesh);

    // Core gold energy ring
    const ringGeom = new THREE.TorusGeometry(heroRadius * 0.88, 3.5, 12, 48);
    const ringMat = new THREE.MeshBasicMaterial({
        color: COLOR_GOLD,
        wireframe: true,
        transparent: true,
        opacity: 0.75
    });
    const ringMesh = new THREE.Mesh(ringGeom, ringMat);
    ringMesh.rotation.x = Math.PI / 3;
    heroGroup.add(ringMesh);

    // Second turquoise counter-rotating ring
    const ring2Geom = new THREE.TorusGeometry(heroRadius * 1.05, 2.5, 12, 48);
    const ring2Mat = new THREE.MeshBasicMaterial({
        color: COLOR_TURQUOISE,
        wireframe: true,
        transparent: true,
        opacity: 0.65
    });
    const ring2Mesh = new THREE.Mesh(ring2Geom, ring2Mat);
    ring2Mesh.rotation.y = Math.PI / 4;
    heroGroup.add(ring2Mesh);

    // 30 Floating Crystal Shards
    const SHARD_COUNT = tier === 'low' ? 16 : 32;
    const shards = [];
    const shardGeom = new THREE.TetrahedronGeometry(Math.max(10, heroRadius * 0.09), 0);
    
    const shardMats = [
        new THREE.MeshPhongMaterial({ color: COLOR_GOLD_BRIGHT, emissive: 0x735500, shininess: 80, transparent: true, opacity: 0.88 }),
        new THREE.MeshPhongMaterial({ color: COLOR_PURPLE, emissive: 0x3d107a, shininess: 60, transparent: true, opacity: 0.82 }),
        new THREE.MeshPhongMaterial({ color: COLOR_TURQUOISE, emissive: 0x0a524a, shininess: 100, transparent: true, opacity: 0.90 })
    ];

    for (let i = 0; i < SHARD_COUNT; i++) {
        const mat = shardMats[i % shardMats.length];
        const shard = new THREE.Mesh(shardGeom, mat);
        
        const orbitRadius = heroRadius * (1.15 + Math.random() * 0.65);
        const theta = (i / SHARD_COUNT) * Math.PI * 2 + (Math.random() * 0.4);
        const phi = (Math.random() - 0.5) * Math.PI * 0.85;
        
        shard.position.set(
            orbitRadius * Math.cos(theta) * Math.cos(phi),
            orbitRadius * Math.sin(phi),
            orbitRadius * Math.sin(theta) * Math.cos(phi)
        );
        
        shard.userData = {
            baseRadius: orbitRadius,
            speedTheta: (0.35 + Math.random() * 0.65) * (i % 2 === 0 ? 1 : -1),
            speedPhi: (0.2 + Math.random() * 0.3) * (i % 3 === 0 ? 1 : -1),
            rotSpeedX: Math.random() * 2.5,
            rotSpeedY: Math.random() * 2.5,
            theta: theta,
            phi: phi
        };
        
        heroGroup.add(shard);
        shards.push(shard);
    }

    function updateHeroPosition() {
        if (width >= 1024) {
            // Right-aligned behind/beside hero text
            heroGroup.position.set(width * 0.22, height * 0.04, -40);
        } else if (width >= 768) {
            heroGroup.position.set(width * 0.18, height * 0.08, -60);
        } else {
            // Centered on mobile behind hero title
            heroGroup.position.set(0, height * 0.12, -90);
        }
    }
    updateHeroPosition();

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

    // ─── Rich Multi-Depth 3D Starry Night Sky [Section 2] ─────────────────
    // 1. Foreground Twinkling Stars (Large, vibrant, high-glow)
    const FG_STARS = tier === 'low' ? 180 : (tier === 'medium' ? 350 : 500);
    const fgGeom = new THREE.BufferGeometry();
    const fgPos = new Float32Array(FG_STARS * 3);
    const fgCol = new Float32Array(FG_STARS * 3);
    const fgSizes = new Float32Array(FG_STARS);

    const starColors = [
        new THREE.Color(0xffffff),      // Brilliant diamond
        new THREE.Color(COLOR_GOLD_BRIGHT), // Neon Gold
        new THREE.Color(COLOR_TURQUOISE),   // Neon Turquoise
        new THREE.Color(0xa855f7)       // Radiant Purple
    ];

    for (let i = 0; i < FG_STARS; i++) {
        fgPos[i * 3 + 0] = (Math.random() - 0.5) * width * 2.2;
        fgPos[i * 3 + 1] = (Math.random() - 0.5) * height * 2.5;
        fgPos[i * 3 + 2] = -Math.random() * 650 + 150;

        const c = starColors[i % starColors.length];
        fgCol[i * 3 + 0] = c.r;
        fgCol[i * 3 + 1] = c.g;
        fgCol[i * 3 + 2] = c.b;

        fgSizes[i] = 1.6 + Math.random() * 1.6; // 1.6px to 3.2px sharp distant stars
    }

    fgGeom.setAttribute('position', new THREE.BufferAttribute(fgPos, 3));
    fgGeom.setAttribute('color', new THREE.BufferAttribute(fgCol, 3));

    const fgMat = new THREE.PointsMaterial({
        size: 2.2,
        vertexColors: true,
        transparent: true,
        opacity: 0.95,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const fgStarfield = new THREE.Points(fgGeom, fgMat);
    backdropGroup.add(fgStarfield);

    // 2. Deep Space Background Constellations (High depth density)
    const BG_STARS = tier === 'low' ? 300 : (tier === 'medium' ? 600 : 900);
    const bgGeom = new THREE.BufferGeometry();
    const bgPos = new Float32Array(BG_STARS * 3);
    const bgCol = new Float32Array(BG_STARS * 3);

    for (let i = 0; i < BG_STARS; i++) {
        bgPos[i * 3 + 0] = (Math.random() - 0.5) * width * 3.0;
        bgPos[i * 3 + 1] = (Math.random() - 0.5) * height * 3.5;
        bgPos[i * 3 + 2] = -Math.random() * 1800 - 300; // Deep Z-space

        const c = starColors[Math.floor(Math.random() * starColors.length)];
        bgCol[i * 3 + 0] = c.r * 0.95;
        bgCol[i * 3 + 1] = c.g * 0.95;
        bgCol[i * 3 + 2] = c.b * 0.95;
    }

    bgGeom.setAttribute('position', new THREE.BufferAttribute(bgPos, 3));
    bgGeom.setAttribute('color', new THREE.BufferAttribute(bgCol, 3));

    const bgMat = new THREE.PointsMaterial({
        size: 1.4,
        vertexColors: true,
        transparent: true,
        opacity: 0.85,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const bgStarfield = new THREE.Points(bgGeom, bgMat);
    backdropGroup.add(bgStarfield);

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
            spring: 0.14 + (i * 0.012),
            orbitAngle: (i / NUM_DRONES) * Math.PI * 2,
            orbitRadius: 28 + (i % 3) * 12
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
    let isHoveringHero = false;
    let heroSpinVelocity = 1.0;

    // Track mouse move
    window.addEventListener('mousemove', (e) => {
        mouseScreenX = e.clientX;
        mouseScreenY = e.clientY;
        
        // Normalized -1 to +1
        targetParallaxX = (e.clientX / width - 0.5) * 2;
        targetParallaxY = -(e.clientY / height - 0.5) * 2;

        // Check if cursor is over hero section
        const heroEl = document.getElementById('home');
        if (heroEl) {
            const rect = heroEl.getBoundingClientRect();
            isHoveringHero = (e.clientY >= rect.top && e.clientY <= rect.bottom);
        }
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

        updateHeroPosition();
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

        // 1. Hero Core High-Energy Animation [3D-01]
        const targetSpin = isHoveringHero ? 4.2 : 1.0;
        heroSpinVelocity += (targetSpin - heroSpinVelocity) * 0.08;

        heroGroup.rotation.y += delta * 0.65 * heroSpinVelocity;
        heroGroup.rotation.x += delta * 0.40 * (isHoveringHero ? 1.5 : 0.8);
        ringMesh.rotation.z += delta * 1.8 * heroSpinVelocity;
        ring2Mesh.rotation.z -= delta * 1.4 * heroSpinVelocity;

        // Tilt toward cursor
        heroGroup.rotation.y += currentParallaxX * 0.03;
        heroGroup.rotation.x += -currentParallaxY * 0.03;

        // React to scroll: drift back and rotate as visitor scrolls past hero
        const heroScrollFactor = Math.min(scrollY / (height * 1.2), 1.0);
        heroGroup.position.z = (width >= 1024 ? -40 : -90) - heroScrollFactor * 450;
        heroGroup.position.y = (width >= 1024 ? height * 0.04 : height * 0.12) + heroScrollFactor * 220;
        heroGroup.scale.setScalar(Math.max(0.4, 1.0 - heroScrollFactor * 0.5));

        // Shards orbit
        for (let i = 0; i < shards.length; i++) {
            const shard = shards[i];
            const ud = shard.userData;
            
            ud.theta += delta * ud.speedTheta * heroSpinVelocity;
            ud.phi += delta * ud.speedPhi;
            
            shard.position.x = ud.baseRadius * Math.cos(ud.theta) * Math.cos(ud.phi);
            shard.position.y = ud.baseRadius * Math.sin(ud.phi);
            shard.position.z = ud.baseRadius * Math.sin(ud.theta) * Math.cos(ud.phi);
            
            shard.rotation.x += delta * ud.rotSpeedX * heroSpinVelocity;
            shard.rotation.y += delta * ud.rotSpeedY * heroSpinVelocity;
        }

        // 2. Cyber Backdrop Perspective Drift [3D-02]
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

        // 3. 3D Drones Positioning & Dynamics [3D-04]
        // Synchronize with window.swarm if present, else follow cursor with orbit
        const swarmActive = (window.swarm && typeof window.swarm.getDots === 'function');
        const swarmAssigned = (window.swarm && typeof window.swarm.isAssigned === 'function' && window.swarm.isAssigned());
        
        // Convert screen (CSS px) to 3D world coordinates at z = 0
        // Screen (0,0) is top-left; in 3D (0,0) is center, Y is positive UP
        const cursorWorldX = mouseScreenX - width * 0.5;
        const cursorWorldY = -(mouseScreenY - height * 0.5);

        for (let i = 0; i < NUM_DRONES; i++) {
            const drone = drones[i];
            const ud = drone.userData;

            // Spin rotor fin
            ud.fin.rotation.y += delta * 22;

            let targetX, targetY, targetZ;

            if (swarmActive && swarmAssigned) {
                // Crew mode / Bot-build phase: read coordinated target positions
                const swarmDots = window.swarm.getDots();
                if (swarmDots && swarmDots[i]) {
                    const dotData = swarmDots[i];
                    targetX = dotData.currentX - width * 0.5;
                    targetY = -(dotData.currentY - height * 0.5);
                    targetZ = 60 + Math.sin(now * 0.004 + i) * 15;
                } else {
                    targetX = cursorWorldX;
                    targetY = cursorWorldY;
                    targetZ = 40;
                }
            } else {
                // Normal follow cursor with organic orbit
                const orbitSpeed = 1.2 + (i % 3) * 0.4;
                const angle = ud.orbitAngle + now * 0.0015 * orbitSpeed;
                const ox = Math.cos(angle) * ud.orbitRadius;
                const oy = Math.sin(angle * 1.3) * (ud.orbitRadius * 0.7);
                
                targetX = cursorWorldX + ox;
                targetY = cursorWorldY + oy;
                targetZ = 40 + Math.sin(angle * 2) * 20;
            }

            // Spring follow
            ud.worldX += (targetX - ud.worldX) * ud.spring;
            ud.worldY += (targetY - ud.worldY) * ud.spring;
            ud.worldZ += (targetZ - ud.worldZ) * 0.12;

            drone.position.set(ud.worldX, ud.worldY, ud.worldZ);

            // Tilt toward movement direction
            const vx = (targetX - ud.worldX) * 0.03;
            const vy = (targetY - ud.worldY) * 0.03;
            drone.rotation.z = -Math.max(-0.45, Math.min(0.45, vx));
            drone.rotation.x = Math.max(-0.35, Math.min(0.35, vy));
            drone.rotation.y = Math.sin(now * 0.002 + i) * 0.25;
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
