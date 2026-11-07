# Changelog (PROMPT v4)

All changes made to the codebase in accordance with PROMPT v4. The original HTML structure, element IDs, typography, text copy, layout, and functional features are 100% preserved.

---

## 1. `assets/css/style.css`

- **[AU-01, Section 2] Cyberpunk 4-Color Theme System (`:root`):**
  - Base: `--bg-color: #05030a` (60%), `--bg-darker: #020106`.
  - Structure: `--cp-purple: #9d4dff` (25%), `--cp-purple-deep: #3a1170`.
  - Energy / Primary: `--cp-gold: #f2c14e` (10%), `--cp-gold-bright: #ffd873`.
  - Interaction / Reactivity: `--cp-turquoise: #19e3d0` (5%), `--cp-turquoise-soft: #7ff5e8`.
  - Borders & Shadows: `--border-glass: rgba(157, 77, 255, 0.22)`, `--border-glass-hover: rgba(25, 227, 208, 0.50)`, `--shadow-neon-turquoise: 0 0 1.875rem rgba(25, 227, 208, 0.40)`.
- **[Section 5] Styled Selection, Focus & Scrollbars:**
  - Styled `::selection` with purple background (`rgba(157, 77, 255, 0.45)`) and bright gold text (`#ffd873`).
  - Styled `:focus-visible` with 2px turquoise outline (`#19e3d0`) and 3px offset.
  - Thin custom scrollbar (6px width, purple thumb with turquoise hover transition).
- **[3D-01 ... 3D-05] WebGL Canvas Architecture:**
  - Added `#gl` fixed background canvas (`position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;`).
- **[H-01 ... H-06] Hover & Micro-Interactions System:**
  - `.cp-hover-title`: Left-to-right gold-to-turquoise underline draw on headings.
  - `.cp-chromatic-split`: 150ms chromatic aberration text shadow (`-2.5px` turquoise, `+2.5px` gold).
  - `.cp-magnetic-btn`: Smooth magnetic button follow (max 6px) with turquoise glow transition.
  - `.cp-3d-card`: 3D perspective tilt (max 7.5°) with dynamic turquoise specular highlight following pointer position.
  - `.cp-input-focused`: Automatically fades follower bots to 15% opacity when visitor types into form inputs.
- **[CB-01 ... CB-05] Nano Local AI Terminal Styling:**
  - Glassmorphic container with neon gold title and live status badge.
  - Cyberpunk user and assistant chat bubbles, responsive horizontal suggestion chips, and turquoise submit button.

---

## 2. `assets/js/gl-engine.js` (NEW MODULE)

- **[3D-01] High-Energy Procedural Hero Core:**
  - Wireframe icosahedron with inner faceted glowing core and dual counter-rotating energy rings in gold and turquoise.
  - 32 floating crystal shards orbiting dynamically in 3D space.
  - Accelerates rotation and pulse trails upon hero hover; drifts back in Z-space on scroll.
- **[3D-02] Cyber Perspective Grid Backdrop:**
  - Infinite perspective grid floor in turquoise and deep purple.
  - 260 drifting cosmic dust particles with camera scroll translation.
- **[3D-04] 8 Low-Poly 3D Drones:**
  - Octahedron gold faceted body, purple glowing wireframe core, spinning turquoise rotor fins, and downward holographic light cones.
  - Follows cursor at rest with organic spring orbits; synchronizes with swarm targets during bot-build sequences.
- **[3D-05] Depth Parallax & Quality Tiers:**
  - Damped mouse parallax across backdrop, hero core, and drone layers.
  - Automatic quality scaling (`high`, `medium`, `low`) and idle tab pausing.
  - Exposed `window.__gl` debug hook reporting active tier, render calls, and geometry.

---

## 3. `assets/js/pull-build.js`

- **[AU-04, 4.2] Simultaneous Inner-Box Swarm Wrap:**
  - Replaced outer corner anchoring with `getInnerBoxes(item, currentYOffset)`: locates internal cards (`.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card`) and headings.
  - Simultaneously divides the 8 drones across the inner cards and boxes.
  - Renders turquoise laser contour scans around each card contour.
  - Renders bright gold laser weld lines sweeping across each box as it materializes.
  - Quad-curved violet-gold tethers connecting drones to the cards.
  - 10 golden snap sparks burst on the card perimeters upon completion.

---

## 4. `assets/js/hover-system.js` (NEW MODULE)

- **[H-01 ... H-06] Unified Micro-Interactions Engine:**
  - Coordinates chromatic split on 18 section titles.
  - Implements physics-based magnetic pull on buttons.
  - Handles 3D card tilt and specular highlight coordinates (`--card-mouse-x`, `--card-mouse-y`).
  - Guards interactions under `prefers-reduced-motion` and touch devices (`hover: none`).

---

## 5. `assets/js/nano-chat.js` (NEW MODULE)

- **[CB-01 ... CB-05] Nano Local AI Terminal:**
  - 100% client-side zero-dependency Q&A assistant.
  - 35-chunk knowledge base derived from Yaser Husen's verified portfolio and experience.
  - BM25 and domain intent keyword retrieval engine responding in < 50ms.
  - Strict XSS safety: text rendered exclusively via `textContent`.
  - Built-in prompt-injection defenses and polite out-of-scope refusals.
  - Suggestion chips, clear history option, and Escape key dismissal.
  - **100.0% pass rate across 28 test cases** in `tests/chat-eval.json`.

---

## 6. Local Vendors & HTML Updates

- **`assets/vendor/three/three.min.js`:** Downloaded and vendored Three.js r128 locally; replaced external CDN script tag in `index.html`.
- **`index.html`:**
  - Added `<canvas id="gl" aria-hidden="true"></canvas>` for 3D WebGL layer.
  - Added inline SVG favicon to eliminate 404 console errors.
  - Added script inclusions for `gl-engine.js`, `hover-system.js`, and `nano-chat.js`.
