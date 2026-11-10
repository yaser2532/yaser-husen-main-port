import math
import struct
import wave
import os

def generate_space_ambient():
    sample_rate = 22050  # 22.05kHz stereo (compact, fast load, pristine sound)
    duration = 40.0      # 40 seconds seamless loop
    num_samples = int(sample_rate * duration)
    num_channels = 2
    sampwidth = 2
    max_amp = 32767 * 0.75

    out_path = "assets/audio/space-ambient.wav"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"Synthesizing {duration}s calm deep space gaming ambient music to {out_path}...")

    # Musical frequencies for deep cosmic tranquility (A minor / Space modal):
    # Bass drone: A1 (55Hz), E2 (82.4Hz), A2 (110Hz)
    # Ethereal mid pads: C3 (130.8Hz), E3 (164.8Hz), G3 (196Hz), B3 (246.9Hz), D4 (293.7Hz)
    # Twinkling celestial overtones: E5 (659.3Hz), B5 (987.8Hz), A5 (880Hz)

    frames = bytearray()

    for i in range(num_samples):
        t = i / sample_rate
        # Loop factor for perfectly seamless 40s loop
        loop_phase = (2 * math.pi * i) / num_samples

        # 1. Deep Sub & Cosmic Drone (A1 + E2 + A2) with slow phase beat
        drone_l = (
            math.sin(2 * math.pi * 55.0 * t) * 0.35 +
            math.sin(2 * math.pi * 82.4 * t + 0.5) * 0.25 +
            math.sin(2 * math.pi * 110.0 * t + 0.2) * 0.20
        )
        drone_r = (
            math.sin(2 * math.pi * 55.2 * t + 0.3) * 0.35 +
            math.sin(2 * math.pi * 82.6 * t + 0.8) * 0.25 +
            math.sin(2 * math.pi * 110.3 * t + 0.6) * 0.20
        )

        # 2. Ethereal Swelling Atmospheric Pad Chords (10s periodic swells)
        swell1 = (math.sin(loop_phase * 4) * 0.5 + 0.5) ** 1.5
        swell2 = (math.cos(loop_phase * 4 + 1.5) * 0.5 + 0.5) ** 1.5

        chord1_l = (
            math.sin(2 * math.pi * 130.8 * t) * 0.15 +
            math.sin(2 * math.pi * 196.0 * t) * 0.12 +
            math.sin(2 * math.pi * 246.9 * t) * 0.10
        ) * swell1

        chord1_r = (
            math.sin(2 * math.pi * 131.0 * t + 0.4) * 0.15 +
            math.sin(2 * math.pi * 196.2 * t + 0.4) * 0.12 +
            math.sin(2 * math.pi * 247.2 * t + 0.4) * 0.10
        ) * swell1

        chord2_l = (
            math.sin(2 * math.pi * 164.8 * t) * 0.14 +
            math.sin(2 * math.pi * 220.0 * t) * 0.11 +
            math.sin(2 * math.pi * 293.7 * t) * 0.08
        ) * swell2

        chord2_r = (
            math.sin(2 * math.pi * 165.0 * t + 0.6) * 0.14 +
            math.sin(2 * math.pi * 220.3 * t + 0.6) * 0.11 +
            math.sin(2 * math.pi * 294.0 * t + 0.6) * 0.08
        ) * swell2

        # 3. Celestial Star-Twinkle Echoes (high register bell/crystal pulses)
        crystal1 = math.sin(2 * math.pi * 659.3 * t) * ((math.sin(loop_phase * 8 + 0.2) * 0.5 + 0.5) ** 6) * 0.09
        crystal2 = math.sin(2 * math.pi * 880.0 * t) * ((math.sin(loop_phase * 6 + 2.0) * 0.5 + 0.5) ** 8) * 0.07
        crystal3 = math.sin(2 * math.pi * 987.8 * t) * ((math.cos(loop_phase * 10 + 1.0) * 0.5 + 0.5) ** 8) * 0.06

        # 4. Soft Cosmic Wind Shimmer (modulated white noise)
        noise_mod = math.sin(loop_phase * 2) * 0.02
        noise_sample = ((i % 73) / 73.0 - 0.5) * 0.015 * (0.8 + noise_mod)

        # Sum audio channels
        left = (drone_l + chord1_l + chord2_l + crystal1 + crystal2 * 0.5 + noise_sample) * 0.62
        right = (drone_r + chord1_r + chord2_r + crystal3 + crystal2 * 0.5 - noise_sample) * 0.62

        # Soft clip limiter
        left = max(-0.95, min(0.95, left))
        right = max(-0.95, min(0.95, right))

        s_left = int(left * max_amp)
        s_right = int(right * max_amp)

        frames.extend(struct.pack('<hh', s_left, s_right))

    with wave.open(out_path, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)

    file_size = os.path.getsize(out_path)
    print(f"Successfully generated {out_path} ({file_size} bytes, {duration}s seamless loop)!")

if __name__ == '__main__':
    generate_space_ambient()
