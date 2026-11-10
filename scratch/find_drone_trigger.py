with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['isSectionEligible', 'checkVisibility', 'startBuild', 'dispatchMission', 'handleScroll']):
        print(f"{i+1}: {line.strip()[:100]}")
