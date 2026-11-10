import shutil
import os

artifact_dir = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

files = [
    ("scratch/test_glitch_hero_char.png", "glitch_hero_char.png"),
    ("scratch/test_glitch_cta_btn.png", "glitch_cta_btn.png"),
    ("scratch/test_glitch_nav_resume.png", "glitch_nav_resume.png"),
    ("scratch/test_glitch_dock_btn.png", "glitch_dock_btn.png"),
    ("scratch/test_kinetic_marquee.png", "kinetic_marquee.png"),
    ("scratch/showcase_project_card_hover.png", "glitch_project_card.png"),
    ("scratch/showcase_project_link_hover.png", "glitch_project_link.png"),
    ("scratch/showcase_filter_btn_hover.png", "glitch_filter_btn.png"),
    ("scratch/showcase_projects_section.png", "glitch_projects_section.png")
]

for src, dst_name in files:
    if os.path.exists(src):
        dst = os.path.join(artifact_dir, dst_name)
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")
    else:
        print(f"Warning: {src} not found!")
