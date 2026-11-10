with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "drone.flightDuration = Math.round(180 + Math.random() * 120); // 180-300ms accelerated return (was 400-650ms)",
    "drone.flightDuration = Math.round(380 + Math.random() * 150); // 380-530ms graceful curved return"
)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated return crew flight duration!")
