import os

html_path = 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize CRLF for operations
content_lf = content.replace('\r\n', '\n')

# 1. Kinetic Cyber Marquee Ticker Strip right at top of page-body-content
marquee_html = """    <!-- Gen Z Kinetic Cyber Marquee Ticker Strip -->
    <div class="cyber-marquee-section" aria-label="High-Velocity Skills & Capabilities Marquee">
        <div class="cyber-marquee-track">
            <!-- First loop of items -->
            <div class="cyber-marquee-group">
                <span class="marquee-item"><i class="fa-solid fa-bolt marquee-star"></i> HIGH-VELOCITY AI PIPELINES</span>
                <span class="marquee-item"><span class="marquee-pill pink">[ENTROPY // 99.4%]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-brain marquee-star"></i> LLM ARCHITECTURE & PROMPT REASONING</span>
                <span class="marquee-item"><span class="marquee-pill">[SYS.STATUS // NOMINAL]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-database marquee-star"></i> ADVANCED SQL & QUANTUM ANALYTICS</span>
                <span class="marquee-item"><span class="marquee-pill gold">⚡ ZERO-LATENCY WEB</span></span>
                <span class="marquee-item"><i class="fa-solid fa-microchip marquee-star"></i> AUTONOMOUS DRONE SWARM ENGINE</span>
                <span class="marquee-item"><span class="marquee-pill purple">[GEN-Z PROTOCOL // ACTIVE]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-code marquee-star"></i> FULL-STACK DATA SCIENCE</span>
                <span class="marquee-item"><span class="marquee-pill pink">0x7F CYBER BUILD</span></span>
            </div>
            <!-- Duplicate loop for seamless infinite marquee wrap -->
            <div class="cyber-marquee-group" aria-hidden="true">
                <span class="marquee-item"><i class="fa-solid fa-bolt marquee-star"></i> HIGH-VELOCITY AI PIPELINES</span>
                <span class="marquee-item"><span class="marquee-pill pink">[ENTROPY // 99.4%]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-brain marquee-star"></i> LLM ARCHITECTURE & PROMPT REASONING</span>
                <span class="marquee-item"><span class="marquee-pill">[SYS.STATUS // NOMINAL]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-database marquee-star"></i> ADVANCED SQL & QUANTUM ANALYTICS</span>
                <span class="marquee-item"><span class="marquee-pill gold">⚡ ZERO-LATENCY WEB</span></span>
                <span class="marquee-item"><i class="fa-solid fa-microchip marquee-star"></i> AUTONOMOUS DRONE SWARM ENGINE</span>
                <span class="marquee-item"><span class="marquee-pill purple">[GEN-Z PROTOCOL // ACTIVE]</span></span>
                <span class="marquee-item"><i class="fa-solid fa-code marquee-star"></i> FULL-STACK DATA SCIENCE</span>
                <span class="marquee-item"><span class="marquee-pill pink">0x7F CYBER BUILD</span></span>
            </div>
        </div>
    </div>
"""

target_marquee_anchor = '<main class="page-body-content">\n'
if target_marquee_anchor in content_lf:
    content_lf = content_lf.replace(target_marquee_anchor, target_marquee_anchor + '\n' + marquee_html + '\n', 1)
    print("Added Kinetic Marquee Ticker Strip.")
else:
    print("Warning: target_marquee_anchor not found!")

# 2. Add telemetry header to Profile & Expertise
target_profile_hdr = """            <div class="section-header">
                <h2 class="section-title">Profile & Expertise</h2>"""

telemetry_profile_hdr = """            <div class="section-header">
                <div class="cyber-telemetry-strip">
                    <span class="telemetry-bracket">[</span>
                    <span>SEC_01 // INTEL_CORE</span>
                    <span class="telemetry-bracket">]</span>
                    <span class="telemetry-pulse"></span>
                    <span class="telemetry-flux">FLUX: 98.8% NOMINAL</span>
                </div>
                <h2 class="section-title">Profile & Expertise</h2>"""

if target_profile_hdr in content_lf:
    content_lf = content_lf.replace(target_profile_hdr, telemetry_profile_hdr, 1)
    print("Added telemetry strip to Profile & Expertise.")

# 3. Add telemetry header to About Me
target_about_hdr = """    <section id="about-me" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">About Me</h2>"""

telemetry_about_hdr = """    <section id="about-me" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <div class="cyber-telemetry-strip">
                    <span class="telemetry-bracket">[</span>
                    <span>SEC_02 // AGENTIC_PROFILE</span>
                    <span class="telemetry-bracket">]</span>
                    <span class="telemetry-pulse"></span>
                    <span class="telemetry-flux">STATUS: ONLINE</span>
                </div>
                <h2 class="section-title">About Me</h2>"""

if target_about_hdr in content_lf:
    content_lf = content_lf.replace(target_about_hdr, telemetry_about_hdr, 1)
    print("Added telemetry strip to About Me.")

# 4. Add telemetry header to Projects
target_proj_hdr = """    <!-- Projects Section -->
    <section id="projects" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Featured Projects</h2>"""

telemetry_proj_hdr = """    <!-- Projects Section -->
    <section id="projects" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <div class="cyber-telemetry-strip">
                    <span class="telemetry-bracket">[</span>
                    <span>SEC_03 // PRODUCTION_BUILDS</span>
                    <span class="telemetry-bracket">]</span>
                    <span class="telemetry-pulse"></span>
                    <span class="telemetry-flux">REGISTRY: 42 NODES</span>
                </div>
                <h2 class="section-title">Featured Projects</h2>"""

if target_proj_hdr in content_lf:
    content_lf = content_lf.replace(target_proj_hdr, telemetry_proj_hdr, 1)
    print("Added telemetry strip to Projects.")

# 5. Add telemetry header to Certifications
target_cert_hdr = """    <!-- Certifications Section -->
    <section id="certificates" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Certifications</h2>"""

telemetry_cert_hdr = """    <!-- Certifications Section -->
    <section id="certificates" class="section-padding scroll-reveal fade-up">
        <div class="container">
            <div class="section-header">
                <div class="cyber-telemetry-strip">
                    <span class="telemetry-bracket">[</span>
                    <span>SEC_04 // CREDENTIAL_VAULT</span>
                    <span class="telemetry-bracket">]</span>
                    <span class="telemetry-pulse"></span>
                    <span class="telemetry-flux">VERIFIED // G-CLOUD</span>
                </div>
                <h2 class="section-title">Certifications</h2>"""

if target_cert_hdr in content_lf:
    content_lf = content_lf.replace(target_cert_hdr, telemetry_cert_hdr, 1)
    print("Added telemetry strip to Certifications.")

# 6. Add Holographic Stickers to project cards
target_card1 = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n                    <div class="project-img-container">'
card1_with_sticker = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n                    <span class="holo-sticker holo-sticker-cyan">⚡ AI-NATIVE</span>\n                    <div class="project-img-container">'

if target_card1 in content_lf:
    content_lf = content_lf.replace(target_card1, card1_with_sticker, 1)
    print("Added holo-sticker 1 to project-card 1.")

target_card2 = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n                    <!-- Visual diagram representing multi-agent orchestration -->'
card2_with_sticker = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n                    <span class="holo-sticker holo-sticker-pink">[PROD // 0x4A]</span>\n                    <!-- Visual diagram representing multi-agent orchestration -->'

if target_card2 in content_lf:
    content_lf = content_lf.replace(target_card2, card2_with_sticker, 1)
    print("Added holo-sticker 2 to project-card 2.")

# Save with CRLF line endings
content_crlf = content_lf.replace('\n', '\r\n')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content_crlf)

print("index.html successfully updated with Gen Z Chaotic elements!")
