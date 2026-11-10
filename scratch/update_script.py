with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check window.__dronesActive for NUM_DOTS
target_num_dots = "const NUM_DOTS = 8;"
replacement_num_dots = "const NUM_DOTS = window.__dronesActive ? 0 : 8;"
assert target_num_dots in content, "NUM_DOTS not found"
content = content.replace(target_num_dots, replacement_num_dots, 1)

# 2. Update startHeroAnimations to avoid re-typing when pre-rendered in HTML
target_hero_anim = """        // Step 1: Type Yaser Husen with authentic human keystrokes
        if (nameCursor) nameCursor.classList.remove('hidden');
        await typeHuman(nameEl, "YASER HUSEN", 85);
        if (nameCursor) nameCursor.classList.add('hidden');

        // Transform into 3D interactive character blocks with mouse physics
        setupHero3dNamePhysics(nameEl);

        // Step 2: Reveal trait tags and about card
        if (detailsContainer) {
            detailsContainer.classList.add('reveal');
        }

        // Step 3: Type description
        if (aboutEl && aboutCursor) {
            aboutCursor.classList.remove('hidden');
            await typeHuman(aboutEl, "I bridge technical data science, scalable artificial intelligence, and high-velocity web platforms to build unified intelligent systems.", 35);
            aboutCursor.classList.add('hidden');
        }"""

replacement_hero_anim = """        // Step 1: Pre-rendered hero text check (Instant 0ms FCP)
        const hasExistingChars = nameEl.querySelectorAll('.hero-3d-char').length > 0;
        if (!hasExistingChars) {
            if (nameCursor) nameCursor.classList.remove('hidden');
            await typeHuman(nameEl, "YASER HUSEN", 85);
            if (nameCursor) nameCursor.classList.add('hidden');
        } else {
            if (nameCursor) nameCursor.classList.add('hidden');
        }

        // Transform into 3D interactive character blocks with mouse physics
        setupHero3dNamePhysics(nameEl);

        // Step 2: Reveal trait tags and about card
        if (detailsContainer) {
            detailsContainer.classList.add('reveal');
        }

        // Step 3: Description setup
        if (aboutEl && aboutCursor) {
            if (!aboutEl.textContent.trim()) {
                aboutCursor.classList.remove('hidden');
                await typeHuman(aboutEl, "I bridge technical data science, scalable artificial intelligence, and high-velocity web platforms to build unified intelligent systems.", 35);
                aboutCursor.classList.add('hidden');
            } else {
                aboutCursor.classList.add('hidden');
            }
        }"""

assert target_hero_anim in content, "target_hero_anim not found"
content = content.replace(target_hero_anim, replacement_hero_anim, 1)

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js successfully!")
