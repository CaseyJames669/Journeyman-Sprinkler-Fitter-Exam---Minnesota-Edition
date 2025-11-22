// ==========================================
// THE FOREMAN'S BRAIN (Game Logic)
// ==========================================

let bankBalance = 0;
let currentIndex = 0;
let currentQueue = [];
let gameMode = 'standard'; // 'standard', 'sudden-death', 'endless'

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

function startGame(mode = 'standard') {
    gameMode = mode;

    // Hide Menu
    document.getElementById('main-menu').style.display = 'none';

    // Show Game UI
    document.getElementById('hud').style.display = 'flex';
    document.getElementById('quiz-card').style.display = 'block';

    // Reset State
    currentQueue = [...questions];
    shuffle(currentQueue);
    currentIndex = 0;
    bankBalance = 0;
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
    document.getElementById('cat-tag').innerText = q.category + (gameMode === 'endless' ? ' (Endless)' : '');
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

    if (isCorrect) {
        btn.classList.add('correct');
        bankBalance += 55; // Journeyman Rate
        speechBubble.innerText = praises[Math.floor(Math.random() * praises.length)];
        speechBubble.style.borderBottom = "4px solid var(--correct)";
        face.style.borderColor = "var(--correct)";
        face.src = "assets/foreman-success.jpg";
    } else {
        btn.classList.add('wrong');

        // Sudden Death Logic
        if (gameMode === 'sudden-death') {
            bankBalance = 0; // You're fired
            updateHUD();
            face.src = "assets/foreman-fail.jpg";
            finishGame("FIRED! One mistake is all it takes.");
            return;
        }

        // Highlight correct
        document.querySelectorAll('.option-btn').forEach(b => {
            if (b.innerText === qData.answer) b.classList.add('missed');
        });
        bankBalance -= 25; // Re-inspection fee
        speechBubble.innerText = roasts[Math.floor(Math.random() * roasts.length)];
        speechBubble.style.borderBottom = "4px solid var(--wrong)";
        face.style.borderColor = "var(--wrong)";
        face.src = "assets/foreman-fail.jpg";
        document.getElementById('quiz-card').classList.add('shaking');
        setTimeout(() => document.getElementById('quiz-card').classList.remove('shaking'), 400);
    }

    speechBubble.style.display = 'block';

    // Show Explanation
    document.getElementById('explanation').style.display = 'block';
    document.getElementById('code-text').innerText = qData.code_text;
    document.getElementById('citation-text').innerText = qData.citation;

    document.getElementById('next-btn').style.display = 'block';
    updateHUD();
}

function nextQuestion() {
    currentIndex++;
    loadQuestion();
}

function updateHUD() {
    const display = document.getElementById('bank-display');
    display.innerText = "$" + bankBalance.toFixed(2);
    display.style.color = bankBalance >= 0 ? "var(--money)" : "var(--wrong)";

    const badge = document.getElementById('rank-badge');
    if (bankBalance < 0) badge.innerText = "Liability";
    else if (bankBalance < 200) badge.innerText = "Green Helper";
    else if (bankBalance < 500) badge.innerText = "Apprentice";
    else badge.innerText = "Journeyman";
}

function finishGame(customMessage = null) {
    document.getElementById('q-text').innerText = customMessage || "Shift Over.";
    document.getElementById('opt-container').innerHTML = "";
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';

    if (customMessage) {
        document.getElementById('foreman-speech').innerText = "Get off my job site.";
        document.getElementById('foreman-speech').style.display = 'block';
    } else {
        document.getElementById('foreman-speech').innerText = bankBalance > 400 ? "Not bad. See you tomorrow." : "Don't quit your day job.";
    }

    const restartBtn = document.createElement('button');
    restartBtn.className = 'btn-next';
    restartBtn.style.display = 'block';
    restartBtn.innerText = "Back to Menu";
    restartBtn.onclick = () => {
        document.getElementById('main-menu').style.display = 'flex';
        document.getElementById('hud').style.display = 'none';
        document.getElementById('quiz-card').style.display = 'none';
        document.getElementById('foreman-speech').style.display = 'none';
        document.getElementById('foreman-img').src = "assets/foreman-loading.jpg";
    };
    document.getElementById('quiz-card').appendChild(restartBtn);
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}
