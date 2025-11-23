// ==========================================
// THE FOREMAN'S BRAIN (Game Logic)
// ==========================================

let bankBalance = 0;
let currentIndex = 0;
let currentQueue = [];
let gameMode = 'standard'; // 'standard', 'sudden-death', 'endless'
let shiftLength = 50; // Default
let correctCount = 0;
let pilotIndices = []; // Indices of questions that don't count (100 Q mode only)
let timerInterval = null;
let timeRemaining = 0; // Seconds

// Audio Assets
const audioCorrect1 = new Audio('audio/absolutely-perfect.mp3');
const audioCorrect2 = new Audio('audio/amazing-i-have-no-anger.mp3');
const audioWrong1 = new Audio('audio/beta-baby.mp3');
const audioWrong2 = new Audio('audio/do-your-parents-know-you-don-t-know-that.mp3');
const audioWrong3 = new Audio('audio/it-s-a-shame.mp3');
const audioGameOver = new Audio('audio/never-never-never-never-ever-ever-ever-ever.mp3');

let isMuted = localStorage.getItem('mn_sprinkler_muted') === 'true';

// Preload Audio
[audioCorrect1, audioCorrect2, audioWrong1, audioWrong2, audioWrong3, audioGameOver].forEach(a => a.load());

const roasts = [
    "My grandmother fits pipe better than that.",
    "You trying to get us red-tagged?",
    "Wrong. Go sit in the truck.",
    "That answer costs money. MY money.",
    "If brains were dynamite, you couldn't blow your nose.",
    "I've seen helpers with hangovers do better.",
    "Are you guessing? Stop guessing.",
    "Wrong. Go sweep the floor."
];

const praises = [
    "Not bad. Keep moving.",
    "Alright, you earned your keep.",
    "Correct. Don't get cocky.",
    "Finally, someone who reads the book.",
    "Good. Now do it faster.",
    "That's the one."
];

const storyHooks = [
    { text: "Fire Marshal's here. I hid the whiskey, you hide the incompetence. Don't get us red-tagged.", img: "assets/scene-inspector.jpg" },
    { text: "The new guy fell down the elevator shaft. Don't look, just work. We're behind schedule.", img: "assets/scene-site.jpg" },
    { text: "Someone hit a main. It's a swimming pool down there. Fix it before the insurance adjuster sees it.", img: "assets/scene-flood.jpg" },
    { text: "Hangover wearing off? Good. Get out there and earn your paycheck before I fire you for breathing too loud.", img: "assets/scene-breakroom.jpg" },
    { text: "I got five hundred riding on you passing this inspection. Don't make me break your legs.", img: "assets/scene-breakroom.jpg" },
    { text: "State inspector is looking for a bribe or a violation. Give him neither.", img: "assets/scene-inspector.jpg" },
    { text: "If you screw this up, you're cleaning the port-a-potties for a month.", img: "assets/scene-site.jpg" }
];

function init() {
    updateMuteIcon();
}

function toggleMute() {
    isMuted = !isMuted;
    localStorage.setItem('mn_sprinkler_muted', isMuted);
    updateMuteIcon();
}

function updateMuteIcon() {
    const btn = document.getElementById('mute-btn');
    if (btn) btn.innerText = isMuted ? "🔇" : "🔊";
}

function playSound(type) {
    if (isMuted) return;

    let clip;
    if (type === 'correct') {
        clip = Math.random() > 0.5 ? audioCorrect1 : audioCorrect2;
    } else if (type === 'wrong') {
        const r = Math.random();
        if (r < 0.33) clip = audioWrong1;
        else if (r < 0.66) clip = audioWrong2;
        else clip = audioWrong3;
    } else if (type === 'gameover') {
        clip = audioGameOver;
    }

    if (clip) {
        clip.currentTime = 0;
        clip.play().catch(e => console.log("Audio play failed", e));
    }
}

function showShiftSelection() {
    document.getElementById('main-menu-options').style.display = 'none';
    document.getElementById('shift-selection').style.display = 'block';
}

function hideShiftSelection() {
    document.getElementById('shift-selection').style.display = 'none';
    document.getElementById('main-menu-options').style.display = 'block';
}

function startGame(mode = 'standard', length = 50) {
    gameMode = mode;

    // Handle Standard Mode Shift Selection
    if (mode === 'standard') {
        shiftLength = length;
    } else {
        shiftLength = 9999; // Endless / Sudden Death
    }

    // Hide Menu
    document.getElementById('main-menu').style.display = 'none';

    // Show Game UI
    document.getElementById('hud').style.display = 'flex';
    document.getElementById('quiz-card').style.display = 'block';

    // Reset State
    currentQueue = [...questions];
    shuffle(currentQueue);

    // Slice queue for standard mode
    if (mode === 'standard') {
        currentQueue = currentQueue.slice(0, shiftLength);

        // Pilot Questions Logic (Only for 100 Q mode)
        pilotIndices = [];
        if (shiftLength === 100) {
            while (pilotIndices.length < 20) {
                let r = Math.floor(Math.random() * 100);
                if (!pilotIndices.includes(r)) pilotIndices.push(r);
            }
            console.log("Pilot Questions (Indices):", pilotIndices);
        }

        // Timer Setup (2 hours for 100 Qs, scaled)
        // 100 Q = 120 min -> 1.2 min/question
        timeRemaining = shiftLength * 1.2 * 60;
        startTimer();
    }

    currentIndex = 0;
    bankBalance = 0;
    correctCount = 0;
    updateHUD();

    // Visual Novel Intro
    const hook = storyHooks[Math.floor(Math.random() * storyHooks.length)];
    document.getElementById('q-text').innerText = `"${hook.text}"`;
    document.getElementById('foreman-img').src = hook.img; // Load Scene Image

    document.getElementById('cat-tag').style.display = 'none';
    document.getElementById('opt-container').innerHTML = ''; // Clear options
    document.getElementById('continue-btn').style.display = 'block'; // Show Continue
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('foreman-speech').style.display = 'none';
    document.getElementById('explanation').style.display = 'none';
}

function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    const display = document.getElementById('rank-badge'); // Reuse badge area for timer in Standard Mode

    timerInterval = setInterval(() => {
        timeRemaining--;

        let mins = Math.floor(timeRemaining / 60);
        let secs = Math.floor(timeRemaining % 60);
        display.innerText = `Time: ${mins}:${secs < 10 ? '0' : ''}${secs}`;

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            finishGame("Time's up! You're too slow.");
        }
    }, 1000);
}

function startQuizFlow() {
    document.getElementById('continue-btn').style.display = 'none';
    document.getElementById('cat-tag').style.display = 'block';
    // Switch back to neutral foreman image
    document.getElementById('foreman-img').src = 'assets/foreman-neutral.jpg';
    loadQuestion();
}

function loadQuestion() {
    // Check for End of Queue
    if (currentIndex >= currentQueue.length) {
        if (gameMode === 'endless') {
            // Endless Mode: Reshuffle and keep going
            shuffle(currentQueue);
            currentIndex = 0;
        } else {
            // Standard/Sudden Death: End Game
            finishGame();
            return;
        }
    }

    const q = currentQueue[currentIndex];

    // Reset UI
    document.getElementById('foreman-speech').style.display = 'none';
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('foreman-img').style.borderColor = "#333";
    document.getElementById('foreman-img').src = "assets/foreman-neutral.jpg";

    // Set Text
    let catText = q.category;
    if (gameMode === 'standard' && shiftLength === 100 && pilotIndices.includes(currentIndex)) {
        // Debug: Mark pilot questions? No, user shouldn't know.
        // catText += " [PILOT]"; 
    }

    document.getElementById('cat-tag').innerText = `${catText} (${currentIndex + 1}/${shiftLength})`;
    document.getElementById('q-text').innerText = q.question;

    // Create Buttons
    const container = document.getElementById('opt-container');
    container.innerHTML = '';

    let opts = [q.answer, ...q.distractors];
    shuffle(opts);

    opts.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = opt;
        btn.onclick = () => handleAnswer(btn, opt === q.answer, q);
        container.appendChild(btn);
    });
}

function handleAnswer(btn, isCorrect, qData) {
    // Disable buttons
    document.querySelectorAll('.option-btn').forEach(b => b.disabled = true);

    const speechBubble = document.getElementById('foreman-speech');
    const face = document.getElementById('foreman-img');

    // Check if this is a pilot question (Standard Mode 100Q only)
    const isPilot = (gameMode === 'standard' && shiftLength === 100 && pilotIndices.includes(currentIndex));

    if (isCorrect) {
        btn.classList.add('correct');
        if (!isPilot) {
            bankBalance += 55; // Journeyman Rate
            correctCount++;
        }

        playSound('correct');
        speechBubble.innerText = praises[Math.floor(Math.random() * praises.length)];
        // speechBubble.style.borderBottom = "4px solid var(--correct)"; // Removed
        face.style.borderColor = "var(--correct)";
        face.src = "assets/foreman-success.jpg";

        // Color the button green
        document.getElementById('next-btn').style.background = "var(--correct)";
        document.getElementById('next-btn').style.color = "#000";
    } else {
        btn.classList.add('wrong');

        // Sudden Death Logic
        if (gameMode === 'sudden-death') {
            playSound('gameover');
            playSuddenDeathVideo();
            return;
        }

        if (!isPilot) {
            bankBalance -= 25; // Re-inspection fee
        }

        playSound('wrong');

        // Highlight correct
        document.querySelectorAll('.option-btn').forEach(b => {
            if (b.innerText === qData.answer) b.classList.add('missed');
        });

        speechBubble.innerText = roasts[Math.floor(Math.random() * roasts.length)];
        // speechBubble.style.borderBottom = "4px solid var(--wrong)"; // Removed
        face.style.borderColor = "var(--wrong)";
        face.src = "assets/foreman-fail.jpg";
        document.getElementById('quiz-card').classList.add('shaking');
        setTimeout(() => document.getElementById('quiz-card').classList.remove('shaking'), 400);

        // Color the button red
        document.getElementById('next-btn').style.background = "var(--wrong)";
        document.getElementById('next-btn').style.color = "#fff";
    }

    speechBubble.style.display = 'block';

    // Show Explanation
    document.getElementById('explanation').style.display = 'block';
    document.getElementById('code-text').innerText = qData.code_text;
    document.getElementById('citation-text').innerText = qData.citation;

    // Show Next Button
    document.getElementById('next-btn').style.display = 'flex';
    updateHUD();
}

function playSuddenDeathVideo() {
    const overlay = document.getElementById('video-overlay');
    const video = document.getElementById('sudden-death-video');

    // Hide game UI to be clean
    document.getElementById('quiz-card').style.display = 'none';
    document.getElementById('hud').style.display = 'none';
    document.getElementById('foreman-speech').style.display = 'none';

    overlay.style.display = 'flex';
    video.currentTime = 0;
    video.play().catch(e => console.error("Video play failed:", e));

    video.onended = () => {
        overlay.style.display = 'none';
        document.getElementById('main-menu').style.display = 'flex';
        document.getElementById('foreman-img').src = 'assets/foreman-loading.jpg';
    };
}

function nextQuestion() {
    currentIndex++;
    loadQuestion();
}

function updateHUD() {
    const display = document.getElementById('bank-display');
    display.innerText = "$" + bankBalance.toFixed(2);
    display.style.color = bankBalance >= 0 ? "var(--money)" : "var(--wrong)";

    if (gameMode !== 'standard') {
        const badge = document.getElementById('rank-badge');
        if (bankBalance < 0) badge.innerText = "Liability";
        else if (bankBalance < 200) badge.innerText = "Green Helper";
        else if (bankBalance < 500) badge.innerText = "Apprentice";
        else badge.innerText = "Journeyman";
    }
}

function finishGame(customMessage = null) {
    if (timerInterval) clearInterval(timerInterval);

    let passed = false;
    let msg = "";
    let subMsg = "";

    if (gameMode === 'standard') {
        // Calculate Score
        // If 100Q mode, we only count non-pilot questions (80 total)
        let totalScored = shiftLength;
        if (shiftLength === 100) totalScored = 80;

        let percent = (correctCount / totalScored) * 100;

        if (percent >= 70) {
            passed = true;
            msg = "SHIFT COMPLETE: PASSED";
            subMsg = `Score: ${percent.toFixed(0)}%. Beers are on me.`;
            playSound('correct');
        } else {
            passed = false;
            msg = "SHIFT COMPLETE: FAILED";
            subMsg = `Score: ${percent.toFixed(0)}%. Go home. See you in 6 months.`;
            playSound('wrong');
        }
    } else {
        msg = "Shift Over.";
        subMsg = bankBalance > 400 ? "Not bad. See you tomorrow." : "Don't quit your day job.";
    }

    if (customMessage) {
        msg = "FIRED";
        subMsg = customMessage;
        playSound('wrong');
    }

    document.getElementById('q-text').innerText = msg;
    document.getElementById('cat-tag').innerText = subMsg;
    document.getElementById('opt-container').innerHTML = "";
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';

    document.getElementById('foreman-speech').innerText = passed ? "Good work." : "Get out of my sight.";
    document.getElementById('foreman-speech').style.display = 'block';

    const restartBtn = document.createElement('button');
    restartBtn.className = 'btn-next';
    restartBtn.style.display = 'block';
    restartBtn.innerText = "Back to Menu";
    restartBtn.onclick = () => {
        location.reload(); // Easiest way to reset everything
    };
    document.getElementById('quiz-card').appendChild(restartBtn);
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Initialize
init();
