# Changelog

All changes made to the codebase in accordance with PROMPT v3. The original HTML structure, element IDs, typography, text copy, layout, and functional features are 100% preserved.

---

## 1. `assets/css/style.css`

- **[A-RECOLOR] Dark Cyberpunk Theme Tokens (`:root`):**
  - Updated `--bg-color` to `#06030c` (near-black with subtle violet undertone).
  - Updated `--bg-darker` to `#030108`.
  - Updated `--card-bg` to `rgba(20, 10, 36, 0.55)` and `--card-bg-hover` to `rgba(34, 16, 58, 0.70)`.
  - Updated `--text-primary` to `#f3eeff`, `--text-secondary` to `#cfc6e6`, `--text-muted` to `#8a7fa8`.
  - Updated `--accent-color` to `#9d4dff` (cyberpunk purple).
  - Updated `--accent-hover` to `#f2c14e` (cyberpunk gold).
  - Updated `--accent-emerald` to `#ffd873` (bright gold).
  - Updated `--shadow-neon-purple` to `0 0 1.875rem rgba(157, 77, 255, 0.35)`.
  - Updated `--shadow-neon-cyan` to `0 0 1.875rem rgba(242, 193, 78, 0.30)`.
  - Updated `--border-glass` to `rgba(157, 77, 255, 0.18)` and hover to `rgba(242, 193, 78, 0.35)`.
- **[A-RECOLOR] Hardcoded Cyan & Blue Replacement:**
  - Replaced hardcoded `#06b6d4`, `#10b981`, and `rgba(6, 182, 212, ...)` across gradients, shadows, text glowing effects, lamp elements, button glows, and modal overlays.
- **[B-01, B-02] Cursor Swarm Visual Upgrade (`.mouse-tracker-dot`):**
  - Replaced flat translucent dots with dual-layer radial gradients: 3–4px bright white-gold core with a 14–18px violet halo.
  - Retained compositor-friendly `transform: translate3d` positioning.
- **[B-04] Touch Device Support:**
  - Enabled dots on touch devices (`@media (hover: none)`), tracking touch events and orbiting lower third of viewport when idle.
- **[C-02, PF-01] Pull-to-Build CSS Architecture (`=== PULL-BUILD (nb-) ===`):**
  - `#nb-canvas`: Fullscreen, fixed pointer-events: none canvas overlay (`z-index: 9998`).
  - `html.nb-ready:not(.nb-done) [data-nb="pending"]`: Sections start hidden via `opacity: 0; transform: translate3d(0, min(90px, 10vh), 0) scale(0.92); pointer-events: none;`.
  - `html.nb-ready [data-nb="pulling"]`: Active pull state with `pointer-events: none;`.
  - `[data-nb="built"]`: Fully settled section restored to `opacity: 1; transform: none; pointer-events: auto;`.
  - `[data-nb="snapping"]::after`: Golden rim flash pseudo-element with 240ms ease-out fade.
  - `html.nb-done`: Restores all sections to native styling and removes canvas visibility.
  - `@media (prefers-reduced-motion: reduce)`: Overrides pending states immediately to full visibility.

---

## 2. `assets/js/script.js`

- **[A-RECOLOR] Scene & Effect Palette Harmonization:**
  - Confetti `COLORS` array updated to purple and gold tones.
  - Three.js starfield particle tints and nebula coloring updated to match the purple-gold theme.
- **[B-02, B-03] Swarm Controller & Crew Mode (`window.swarm`):**
  - Exposed `window.swarm = { assign(targets), release(), isAssigned(), getDots() }`.
  - Added target tracking allowing `pull-build.js` to dispatch dots to section corners during pulls.
  - Retained organic orbit offsets and spring easing during both cursor-following and crew assignment.
- **[B-04] Touch Event Handlers:**
  - Added `touchstart` and `touchmove` listeners to route touch coordinates to the swarm.
  - Added idle center point calculation in the lower third of the viewport when no touch input is active.
- **[B-05, PF-06] Sleep Loop When Idle:**
  - Swarm rAF loop enters sleep mode after 2 seconds of inactivity and wakes automatically on mouse or touch input.
- **[Regression / Parity Hook]:**
  - Exposed `window.animateCounters` so that stat counter numbers animate smoothly when `#about-me` is pulled into view.

---

## 3. `assets/js/threescenes.js`

- **[A-RECOLOR] 3D Cake & Gift Scene Colors:**
  - Updated `sprinkleColors` array from cyan/emerald to gold (`0xf2c14e`), bright gold (`0xffd873`), and purple (`0x9d4dff`).
  - Updated candle materials to harmonized gold and violet tones.

---

## 4. `assets/js/pull-build.js` (NEW MODULE)

- **[C-01 ... C-07] Framework-Agnostic Pull-to-Build Engine:**
  - Written as a self-contained IIFE with 0 external dependencies (11.4 KB minified).
  - Handles 5-phase pull lifecycle:
    1. **Ghost Blueprint (`C-03`):** Renders dashed purple outline (`rgba(157, 77, 255, 0.45)`) on the canvas for pending sections.
    2. **Dispatch Swarm (`C-03`):** Calls `swarm.assign()` to send dots to the section's top/bottom corners.
    3. **Tether Formation (`C-03`):** Draws glowing bezier lines (3px violet glow + 1px gold core) from dots to section anchor points.
    4. **Section Pull (`C-03`):** Interpolates section position from `translate3d(0, 90px, 0) scale(0.92)` to `(0, 0, 0) scale(1.0)` using `cubic-bezier(0.16, 1, 0.3, 1)` easing.
    5. **Snap Sparks (`C-03`):** Releases swarm, triggers 10 gold sparks on the canvas, fires golden rim flash, and staggers `.scroll-reveal` children.
  - **Sequential Order (`C-05`):** Strictly enforces pulling in page order (`#home` -> `#profile-expertise` -> `#about-me` -> `#projects` -> `#creative-lab` -> `#certificates` -> `#secret-desk` -> `#contact`).
  - **Permanence (`C-04`):** Once a section is marked `data-nb="built"`, it never re-animates or un-builds during the session.
  - **Fast Scroll Catch-Up (`C-06`):** Fast scrolling rapidly pulls preceding sections in sequence (180ms fast duration) so the user never encounters broken unbuilt gaps.
  - **End of Page Completion (`C-07`):** Marks `html.nb-done`, releases swarm to cursor, disconnects IntersectionObserver, and sleeps the canvas rAF loop.
  - **Fail-safe Timer (`T-07`):** 3-second failsafe timer ensures all sections are visible even if an unhandled error occurs.
  - **Reduced Motion Support (`T-10`):** Checks `window.matchMedia('(prefers-reduced-motion: reduce)')` and skips all pulling if requested.

---

## 5. `index.html`

- Added `<canvas id="nb-canvas" aria-hidden="true"></canvas>` overlay right after `<body>`.
- Added `<script src="assets/js/pull-build.js"></script>` before the closing `</body>` tag.

---

## 6. Project Configuration

- Updated `.gitignore` to exclude `_baseline/`, `shots/`, `tools/`, and `node_modules/` from deployment builds.
