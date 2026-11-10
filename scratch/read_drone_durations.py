import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 770-800 in drones.js ---")
for j in range(769, 800):
    print(f"{j+1}: {lines[j]}", end="")

print("\n--- Lines 975-990 in drones.js ---")
for j in range(974, 990):
    print(f"{j+1}: {lines[j]}", end="")
