with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update scroll-behavior: smooth -> auto !important
old_sb = """html {

    scroll-behavior: smooth;

}"""
new_sb = """html {

    scroll-behavior: auto !important;

}"""

if old_sb in content:
    content = content.replace(old_sb, new_sb)
    print("Replaced scroll-behavior on html")
else:
    print("Could not find exact old_sb")

# 2. In lines 9940-9951:
# .contact-card,\n.profile-card-wrapper {
target_2 = ".contact-card,\n.profile-card-wrapper {"
repl_2 = ".contact-card {"
count_target_2 = content.count(target_2)
print(f"Occurrences of target_2: {count_target_2}")
content = content.replace(target_2, repl_2)

# 3. In lines 10025-10038:
# .profile-card-wrapper:hover,\n.cp-3d-card:hover {
target_3 = ".profile-card-wrapper:hover,\n.cp-3d-card:hover {"
repl_3 = ".cp-3d-card:hover {"
if target_3 in content:
    content = content.replace(target_3, repl_3)
    print("Replaced target_3")
else:
    print("target_3 not found")

# 6. In lines 10453-10474:
# .profile-card-wrapper:hover,\n.card-3d-active {
target_6 = ".profile-card-wrapper:hover,\n.card-3d-active {"
repl_6 = ".card-3d-active {"
if target_6 in content:
    content = content.replace(target_6, repl_6)
    print("Replaced target_6")
else:
    print("target_6 not found")

# 7. Add dedicated circular profile styling and update html/body overflow
profile_block = """
/* =========================================================================
   PROFILE IMAGE CIRCULAR FRAME WITH GRADIENT COLOR BORDER
   Clean, circular frame with cyber gradient border and soft glow
   ========================================================================= */
.profile-card-wrapper {
    position: relative !important;
    width: 18.75rem !important;
    height: 18.75rem !important;
    border-radius: 50% !important;
    padding: 5px !important;
    background: linear-gradient(135deg, #19E3D1 0%, #FF1E42 32%, #9D4DFF 65%, #F5C542 100%) !important;
    box-shadow: 
        0 0 25px rgba(25, 227, 209, 0.45),
        0 0 50px rgba(157, 77, 255, 0.35),
        0 0 18px rgba(255, 30, 66, 0.35) !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease !important;
    overflow: hidden !important;
}

.profile-card-wrapper:hover {
    transform: scale(1.04) !important;
    box-shadow: 
        0 0 35px rgba(25, 227, 209, 0.65),
        0 0 70px rgba(157, 77, 255, 0.55),
        0 0 30px rgba(255, 30, 66, 0.55),
        0 0 100px rgba(245, 197, 66, 0.35) !important;
}

.profile-details-img {
    width: 100% !important;
    height: 100% !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    display: block !important;
    border: 3px solid #0d0818 !important;
    background-color: #0d0818 !important;
}

@media (max-width: 768px) {
    .profile-card-wrapper {
        width: 15rem !important;
        height: 15rem !important;
    }
}
"""

# Replace overflow block
old_overflow = """html, body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
}"""

new_overflow = """html {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: clip !important;
    box-sizing: border-box !important;
}

body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    -webkit-overflow-scrolling: touch;
    box-sizing: border-box !important;
}"""

if old_overflow in content:
    content = content.replace(old_overflow, new_overflow + "\n" + profile_block)
    print("Replaced overflow block and appended profile styling")
else:
    print("old_overflow not found")
    content += "\n" + profile_block

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating style.css")
