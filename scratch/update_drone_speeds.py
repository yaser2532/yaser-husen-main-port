with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(782, 803):
    if 'let pullDuration = 180;' in lines[i]:
        lines[i] = '                let pullDuration = 280; // Card pull: 280ms (reduced speed by 0.1s)\n'
        print(f"Updated line {i+1} to 280ms")
    elif 'pullDuration = 400;' in lines[i]:
        lines[i] = '                    pullDuration = 500; // Title scanline sweep: 500ms (reduced speed by 0.1s)\n'
        print(f"Updated line {i+1} to 500ms")
    elif 'pullDuration = 250;' in lines[i] and 'Paragraph' in lines[i]:
        lines[i] = '                    pullDuration = 350; // Paragraph line sweep: 350ms (reduced speed by 0.1s)\n'
        print(f"Updated line {i+1} to 350ms")
    elif 'pullDuration = 150;' in lines[i]:
        lines[i] = '                    pullDuration = 250; // Button/link snap-in: 250ms (reduced speed by 0.1s)\n'
        print(f"Updated line {i+1} to 250ms")
    elif 'pullDuration = 250;' in lines[i] and 'Frame' in lines[i]:
        lines[i] = '                    pullDuration = 350; // Frame 350ms, then lines 50ms each (reduced speed by 0.1s)\n'
        print(f"Updated line {i+1} to 350ms")

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS: drones.js pull durations updated!")
