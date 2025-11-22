// ==========================================
// THE FOREMAN'S BRAIN (Game Logic)
// ==========================================

let bankBalance = 0;
let currentIndex = 0;
let currentQueue = [];

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

async function startGame() {
    // Ensure `questions` is available. Prefer pre-bundled `js/questions.js` but
    // fall back to fetching `all_questions.json` if the variable is not present.
    if (typeof questions === 'undefined' || !Array.isArray(questions) || questions.length === 0) {
        try {
            const resp = await fetch('all_questions.json');
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            window.questions = await resp.json();
        } catch (err) {
            console.error('Failed to load questions:', err);
            alert('Unable to load question data. See console for details.');
            return;
        }
    }
    // Hide Menu
    document.getElementById('main-menu').style.display = 'none';

    // Show Game UI
    document.getElementById('hud').style.display = 'flex';
    document.getElementById('quiz-card').style.display = 'block';

    // Switch to neutral foreman image
    document.getElementById('foreman-img').src = 'assets/foreman-neutral.jpg';

    currentQueue = [...questions];
    shuffle(currentQueue);
    currentIndex = 0;
    bankBalance = 0;
    updateHUD();
    loadQuestion();
}

function loadQuestion() {
    if (currentIndex >= currentQueue.length) {
        finishGame();
        return;
    }

    const q = currentQueue[currentIndex];

    // Reset UI
    document.getElementById('foreman-speech').style.display = 'none';
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('foreman-img').style.borderColor = "#333";
    document.getElementById('foreman-img').src = "assets/foreman-neutral.jpg";

    // Set Text
    document.getElementById('cat-tag').innerText = q.category;
    document.getElementById('q-text').innerText = q.question;
    // Move focus to the question for keyboard / screen reader users
    const qElem = document.getElementById('q-text');
    if (qElem && typeof qElem.focus === 'function') qElem.focus();

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
    // Move focus to the Next button so keyboard users can continue
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn && typeof nextBtn.focus === 'function') nextBtn.focus();
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

function finishGame() {
    document.getElementById('q-text').innerText = "Shift Over.";
    document.getElementById('opt-container').innerHTML = "";
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('foreman-speech').innerText = bankBalance > 400 ? "Not bad. See you tomorrow." : "Don't quit your day job.";

    const restartBtn = document.createElement('button');
    restartBtn.className = 'btn-next';
    restartBtn.style.display = 'block';
    restartBtn.innerText = "Start New Shift";
    restartBtn.onclick = startGame;
    document.getElementById('quiz-card').appendChild(restartBtn);
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}
