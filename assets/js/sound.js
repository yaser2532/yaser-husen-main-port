// assets/js/sound.js
(function () {
    let audioCtx = null;
    let masterGain = null;
    let isMuted = false;

    // Initialize AudioContext on first user interaction (browser autoplay policy compliance)
    function initAudio() {
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        masterGain = audioCtx.createGain();
        masterGain.gain.setValueAtTime(0.25, audioCtx.currentTime); // default master volume for interactive sounds
        masterGain.connect(audioCtx.destination);
    }

    // Toggle mute state
    function toggleMute() {
        isMuted = !isMuted;
        if (masterGain) {
            masterGain.gain.setValueAtTime(isMuted ? 0 : 0.25, audioCtx ? audioCtx.currentTime : 0);
        }
        
        // Also mute/unmute the HTML5 background music element if it exists
        const bgMusic = document.getElementById('bgMusic');
        if (bgMusic) {
            bgMusic.muted = isMuted;
        }

        // Update UI
        updateSoundButtonUI();
        
        // Save state in localStorage
        localStorage.setItem('portfolio_muted', isMuted ? 'true' : 'false');
    }

    function updateSoundButtonUI() {
        const btn = document.getElementById('sound-toggle-btn');
        if (!btn) return;
        if (isMuted) {
            btn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
            btn.setAttribute('title', 'Unmute Sounds');
            btn.classList.add('muted');
        } else {
            btn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
            btn.setAttribute('title', 'Mute Sounds');
            btn.classList.remove('muted');
        }
    }

    // General play sound function helper
    function playSound(synthFn) {
        initAudio();
        if (isMuted) return;
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        try {
            synthFn();
        } catch (e) {
            console.warn("Could not play sound:", e);
        }
    }

    // Synthesizers
    const synths = {
        // Subtle hover click tick
        hover: () => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(masterGain);

            osc.type = 'sine';
            osc.frequency.setValueAtTime(750, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1000, audioCtx.currentTime + 0.04);

            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.04);

            osc.start();
            osc.stop(audioCtx.currentTime + 0.04);
        },

        // Clean UI click
        click: () => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(masterGain);

            osc.type = 'sine';
            osc.frequency.setValueAtTime(350, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + 0.06);

            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.06);

            osc.start();
            osc.stop(audioCtx.currentTime + 0.06);
        },

        // Mechanical switch click (ON)
        switchOn: () => {
            const osc1 = audioCtx.createOscillator();
            const osc2 = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc1.connect(gain);
            osc2.connect(gain);
            gain.connect(masterGain);

            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(580, audioCtx.currentTime);
            osc2.type = 'triangle';
            osc2.frequency.setValueAtTime(750, audioCtx.currentTime);

            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);

            osc1.start();
            osc2.start();
            osc1.stop(audioCtx.currentTime + 0.05);
            osc2.stop(audioCtx.currentTime + 0.05);
        },

        // Mechanical switch click (OFF)
        switchOff: () => {
            const osc1 = audioCtx.createOscillator();
            const osc2 = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc1.connect(gain);
            osc2.connect(gain);
            gain.connect(masterGain);

            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(420, audioCtx.currentTime);
            osc2.type = 'triangle';
            osc2.frequency.setValueAtTime(320, audioCtx.currentTime);

            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);

            osc1.start();
            osc2.start();
            osc1.stop(audioCtx.currentTime + 0.05);
            osc2.stop(audioCtx.currentTime + 0.05);
        },

        // Cheerful major chord arpeggio for success
        success: () => {
            const now = audioCtx.currentTime;
            const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
            notes.forEach((freq, idx) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(masterGain);

                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + idx * 0.06);

                gain.gain.setValueAtTime(0, now);
                gain.gain.setValueAtTime(0.15, now + idx * 0.06);
                gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.22);

                osc.start(now + idx * 0.06);
                osc.stop(now + idx * 0.06 + 0.22);
            });
        },

        // Error double beep
        error: () => {
            const now = audioCtx.currentTime;
            [0, 0.12].forEach((delay) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(masterGain);

                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(140, now + delay);

                gain.gain.setValueAtTime(0.2, now + delay);
                gain.gain.exponentialRampToValueAtTime(0.001, now + delay + 0.12);

                osc.start(now + delay);
                osc.stop(now + delay + 0.12);
            });
        },

        // Cosmic / magic sweep for fortune ball and constellations
        magic: () => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(masterGain);

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(260, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1400, audioCtx.currentTime + 0.75);

            // Add slight LFO for vibrato
            const lfo = audioCtx.createOscillator();
            const lfoGain = audioCtx.createGain();
            lfo.frequency.value = 16; 
            lfoGain.gain.value = 25; 
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);

            gain.gain.setValueAtTime(0.18, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.12, audioCtx.currentTime + 0.5);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.75);

            lfo.start();
            osc.start();
            lfo.stop(audioCtx.currentTime + 0.75);
            osc.stop(audioCtx.currentTime + 0.75);
        },

        // Pop sound for gift open
        pop: () => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(masterGain);

            osc.type = 'sine';
            osc.frequency.setValueAtTime(160, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(550, audioCtx.currentTime + 0.18);

            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.18);

            osc.start();
            osc.stop(audioCtx.currentTime + 0.18);
        },

        // Soft breath wind woosh for blowing candles
        blow: () => {
            const bufferSize = audioCtx.sampleRate * 0.45;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }

            const noiseSource = audioCtx.createBufferSource();
            noiseSource.buffer = buffer;

            const filter = audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(700, audioCtx.currentTime);
            filter.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.45);

            const gain = audioCtx.createGain();
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.45);

            noiseSource.connect(filter);
            filter.connect(gain);
            gain.connect(masterGain);

            noiseSource.start();
            noiseSource.stop(audioCtx.currentTime + 0.45);
        }
    };

    // Expose sound playback interface globally
    window.PortfolioSounds = {
        playHover: () => playSound(synths.hover),
        playClick: () => playSound(synths.click),
        playSwitchOn: () => playSound(synths.switchOn),
        playSwitchOff: () => playSound(synths.switchOff),
        playSuccess: () => playSound(synths.success),
        playError: () => playSound(synths.error),
        playMagic: () => playSound(synths.magic),
        playPop: () => playSound(synths.pop),
        playBlow: () => playSound(synths.blow),
        toggleMute: toggleMute,
        isMuted: () => isMuted
    };

    // Setup global floating mute/unmute UI and default state
    document.addEventListener('DOMContentLoaded', () => {
        // Load mute state from storage
        const savedMuted = localStorage.getItem('portfolio_muted');
        if (savedMuted === 'true') {
            isMuted = true;
        }

        // Create the floating button
        const soundBtn = document.createElement('button');
        soundBtn.id = 'sound-toggle-btn';
        soundBtn.className = 'sound-toggle-btn';
        document.body.appendChild(soundBtn);

        updateSoundButtonUI();

        // Bind button action
        soundBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            initAudio();
            toggleMute();
            
            // Play a small click on unmute
            if (!isMuted) {
                window.PortfolioSounds.playClick();
            }
        });

        // Initialize state on background music if already loaded
        const bgMusic = document.getElementById('bgMusic');
        if (bgMusic) {
            bgMusic.muted = isMuted;
        }

        // Attach event listeners for Hover and Click sounds using event delegation
        const interactiveSelectors = [
            'a', 
            'button', 
            '.project-card', 
            '.cert-card', 
            '.filter-btn', 
            '.back-to-top',
            '#lamp-toggle',
            '.crystal-ball'
        ];

        // Delegated mouseenter/hover sound (using capture since mouseenter doesn't bubble)
        document.body.addEventListener('mouseenter', (e) => {
            const target = e.target.closest && e.target.closest(interactiveSelectors.join(','));
            if (target && target.id !== 'sound-toggle-btn') {
                window.PortfolioSounds.playHover();
            }
        }, true);

        // Delegated click sound
        document.body.addEventListener('click', (e) => {
            const target = e.target.closest && e.target.closest(interactiveSelectors.join(','));
            if (target && target.id !== 'sound-toggle-btn') {
                if (target.id === 'lamp-toggle') {
                    // Switch toggle uses custom dual tone click
                    const isChecked = target.checked;
                    if (isChecked) {
                        window.PortfolioSounds.playSwitchOn();
                    } else {
                        window.PortfolioSounds.playSwitchOff();
                    }
                } else if (target.id === 'btnStart' || target.id === 'celebrateBtn' || target.id === 'submit-btn') {
                    // Custom action clicks can trigger their own specific sounds
                    window.PortfolioSounds.playClick();
                } else if (target.classList.contains('crystal-ball') || target.id === 'crystalBall') {
                    window.PortfolioSounds.playMagic();
                } else if (target.id === 'giftCanvas') {
                    window.PortfolioSounds.playPop();
                } else {
                    window.PortfolioSounds.playClick();
                }
            }
        });
    });
})();
