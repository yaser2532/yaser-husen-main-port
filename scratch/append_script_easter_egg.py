with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

easter_egg_code = """
// ════════════════════════════════════════════════════════════
//  GEN Z TORN PAPER & CRT STATIC NOISE EASTER EGGS MODULE
// ════════════════════════════════════════════════════════════
function initEasterEggStaticNoise() {
    const overlay = document.getElementById('static-noise-overlay');
    const canvas = document.getElementById('static-noise-canvas');
    const toastMsg = document.getElementById('static-toast-msg');
    if (!overlay || !canvas) return;

    const ctx = canvas.getContext('2d');
    let animId = null;
    let isStaticActive = false;

    function resizeStaticCanvas() {
        canvas.width = Math.round(window.innerWidth * 0.5);
        canvas.height = Math.round(window.innerHeight * 0.5);
    }
    resizeStaticCanvas();
    window.addEventListener('resize', resizeStaticCanvas, { passive: true });

    function renderStaticNoiseFrame() {
        if (!isStaticActive) return;
        const w = canvas.width;
        const h = canvas.height;
        const imgData = ctx.createImageData(w, h);
        const buffer = new Uint32Array(imgData.data.buffer);
        const len = buffer.length;

        for (let i = 0; i < len; i++) {
            const rand = Math.random();
            if (rand < 0.04) {
                buffer[i] = 0xffd1e319; // Cyan glitch pixel
            } else if (rand < 0.08) {
                buffer[i] = 0xff852aff; // Pink glitch pixel
            } else {
                const gray = (Math.random() * 255) | 0;
                buffer[i] = (0xff << 24) | (gray << 16) | (gray << 8) | gray;
            }
        }
        ctx.putImageData(imgData, 0, 0);
        animId = requestAnimationFrame(renderStaticNoiseFrame);
    }

    function playStaticCrackle() {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const actx = new AudioCtx();
            if (actx.state === 'suspended') {
                actx.resume();
            }
            const bufferSize = Math.round(actx.sampleRate * 0.18);
            const noiseBuffer = actx.createBuffer(1, bufferSize, actx.sampleRate);
            const output = noiseBuffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                output[i] = (Math.random() * 2 - 1) * 0.06;
            }
            const whiteNoise = actx.createBufferSource();
            whiteNoise.buffer = noiseBuffer;
            const filter = actx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 1200;
            whiteNoise.connect(filter);
            filter.connect(actx.destination);
            whiteNoise.start();
        } catch (e) {
            // Fallback safely
        }
    }

    const EASTER_EGG_MESSAGES = {
        chaos: '⚡ CHAOS DETECTED: "Entropy Overclocked to 420% // Neural Sync Active!"',
        static: '📺 CRT VINTAGE TV STATIC: "Zero Data Noise · ATTF Cleaned 100% of Junk Records!"',
        code: '⚡ DEV MEMO: "Automated Review Passed: 0 Bugs, 100% Test Coverage!"',
        entropy: '🎂 CELEBRATION PROTOCOL: "Unlimited Joy & Good Vibes Activated for 2026!"',
        secret: '✨ SECRET FOUND: "You discovered Yaser Husen\'s hidden cyber vault!"'
    };

    window.triggerStaticGlitch = function(type = 'chaos', customMsg = '') {
        isStaticActive = true;
        overlay.classList.add('active');
        if (toastMsg) {
            toastMsg.textContent = customMsg || EASTER_EGG_MESSAGES[type] || '⚡ EASTER EGG UNLOCKED // CHAOS CORE';
        }
        playStaticCrackle();
        cancelAnimationFrame(animId);
        renderStaticNoiseFrame();

        setTimeout(() => {
            isStaticActive = false;
            overlay.classList.remove('active');
            cancelAnimationFrame(animId);
        }, 700);
    };

    document.querySelectorAll('.torn-paper-sticker').forEach(sticker => {
        sticker.addEventListener('click', (e) => {
            e.stopPropagation();
            const eggType = sticker.getAttribute('data-easter-egg') || 'chaos';
            window.triggerStaticGlitch(eggType);
        });
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEasterEggStaticNoise);
} else {
    initEasterEggStaticNoise();
}
"""

if "initEasterEggStaticNoise" not in code:
    code = code + "\n" + easter_egg_code

with open('assets/js/script.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(code.replace('\r\n', '\n').replace('\n', '\r\n'))

print("Updated assets/js/script.js successfully!")
