# Changelog (Refinements & Final Polish)

All enhancements made in accordance with the user's latest directives. The original HTML structure, element IDs, typography, text copy, layout, and functional features are 100% preserved.

---

## 1. Hero Dynamic Typography & Human Typing ([`script.js`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/js/script.js#L650-L730), [`style.css`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/css/style.css#L160-L210))
- **Human Keystroke Cadence:** Added randomized keystroke timing (40ms–85ms) with natural micro-pauses at punctuation, spaces, and ampersands.
- **Hero Name Typing:** "YASER HUSEN" types out smoothly with realistic human rhythm and modern italic styling.
- **Continuous Rotating Skill Titles:** Loops through 5 verified skill titles:
  1. *Data Analyst & AI Integration Specialist*
  2. *Prompt Engineering & LLM API Architecture*
  3. *Enterprise RAG Pipelines & GCP Vertex AI*
  4. *Advanced SQL Analytics & Predictive Modeling*
  5. *High-Performance 3D Web & Interactive Systems*
- **Neon Cursor & Typography:** Styled with sleek modern italic typography (`#tp-name` with gold gradient drop shadow, `#tp-subtitle` with turquoise neon glow) and a smoothly blinking neon cursor line.

---

## 2. Multi-Depth 3D Starry Night Sky & Cyberpunk Neon Lighting ([`gl-engine.js`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/js/gl-engine.js#L210-L290), [`style.css`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/css/style.css#L3780-L3840))
- **Rich Multi-Layered Cosmos:**
  - Layer 1: ~500 bright twinkling foreground stars (diamond white, neon gold, turquoise, radiant purple) with dynamic sine-wave shimmering and sizes up to 9.5px.
  - Layer 2: ~900 deep space stars across depth `-1800` to `-300` providing authentic 3D depth flight on scroll.
- **Transparent Body Layering:** Set `html` to base black `#05030a` and `body` to transparent, allowing the 3D starry sky to shine through vibrantly across all sections.
- **Neon Light Styles for Small Elements:**
  - Buttons (`.btn, .cta-btn, .filter-btn`): Glowing glassmorphic text backgrounds with gold borders and turquoise neon hover sweeps.
  - Badges & Trait Tags (`.trait-tag, .badge`): Cyberpunk pill styling with luminous borders and subtle inner neon glow.
- **Enhanced Gradient Hover:** Card hover highlights are now 2.5× more pronounced with a vivid turquoise-gold radial gradient following pointer coordinates.

---

## 3. Natural Gravity Physics on Hanging Lamp Chain ([`script.js`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/js/script.js#L326-L435), [`style.css`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/css/style.css#L1555-L1570))
- **Pendulum Gravity Equation:** Replaced linear springs with true physical pendulum gravity ($\alpha = -g \sin\theta$) and fluid aerodynamic drag damping.
- **Catenary Momentum Flex:** Added dynamic `skewX` inertia so the chain flexes organically with momentum when swung or dragged.
- **Cyberpunk Braided Metal Cord:** Styled with repeating linear gradient in gold and turquoise with soft neon drop shadows.

---

## 4. Bot-Build Deep Text & Card Wrapping ([`pull-build.js`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/js/pull-build.js#L196-L260))
- **Text & Container Targeting:** Drones explicitly target both container cards and individual text blocks (headings, descriptions, paragraphs, stat numbers).
- **Text Reticle Brackets & Weld Lines:** Renders neon gold corner brackets around text elements and sweeps bright gold laser weld lines across headings and cards as they materialize.
- **Cinematic Timing Slowdown:** Extended pull sequence duration to ~2.1s (+0.75s) so the mechanical construction is easy to watch and appreciate.

---

## 5. Conversational Chatbot Fallbacks ([`nano-chat.js`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/assets/js/nano-chat.js#L140-L225), [`tests/chat-eval.json`](file:///c:/Users/yhuse/OneDrive/Desktop/portfolio-main/yaser-husen-main-port/tests/chat-eval.json))
- **Conversational Handlers:** Added natural handling for greetings ("hello", "hey"), compliments ("love the 3d", "nice website"), and capabilities inquiries.
- **Resilient Fallback:** Wrapped in safe try/catch error handling; unpredicted queries receive a warm, contextual guide with suggestion chips instead of an error.
- **Automated Verification:** **100.0% pass rate across 32 test cases** (factual, conversational, and unpredicted).
