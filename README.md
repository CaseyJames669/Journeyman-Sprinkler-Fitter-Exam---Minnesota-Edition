# MN Sprinkler Fitter Exam Prep (Mobile App)

**A gamified study tool for the Minnesota Journeyman Sprinkler Fitter Exam.**

Designed for **Android & iOS** (via Capacitor) and works offline in any modern browser.

---

## 📱 Features

### **Mobile First Design**
- **Touch-Optimized**: Big buttons, clear text, and a UI designed for thumbs.
- **Offline Ready**: All questions are pre-loaded. No internet required after installation.
- **Installable**: Add to Home Screen as a PWA or build as a native app.

### **Game Modes**
1. **Standard Shift (Exam Sim)**
   - **Choose Your Shift**: 10, 25, 50, or **100 Questions**.
   - **Real Exam Mode (100 Qs)**: Simulates the actual test. **20 random questions are "pilot" questions** that don't count toward your score (just like the real thing), but you won't know which ones they are!
   - **Time Limit**: 2 Hours for the full 100-question exam (scaled down for shorter shifts).
   - **The Stakes**:
     - **Pass (70%+)**: The Foreman buys you beers. 🍻
     - **Fail (<70%) or Time Out**: You get sent home for 6 months. 🚫

2. **Sudden Death**
   - **One Strike & You're Out**.
   - See how far you can get before making a single mistake.
   - High stakes, high pressure.

3. **Endless Mode**
   - Just work. No timer, no pressure. Good for casual study.

### **Resource Center (New!)**
- **Code Lookup**: A searchable database of all questions, codes, and citations.
- **Study Tool**: Quickly find rules on spacing, hangers, calc, etc. without taking a quiz.

### **The Foreman (Audio & Visuals)**
- **Dynamic Feedback**: The Foreman reacts to your performance.
- **Audio**:
  - **Correct**: "Perfect", "No Anger".
  - **Wrong**: "Beta", "Do you know?", "It's a shame".
  - **Game Over**: "Never Ever".
- **Mute Button**: Toggle sound on/off in the HUD.

---

## 🛠 Project Structure

- `index.html`: Main entry point (Game Menu).
- `resources.html`: Searchable Code/Question database.
- `js/game.js`: Core game logic (Modes, Timer, Audio, Scoring).
- `js/questions.js`: **Crucial**. Contains the entire question bank as a global variable for offline access.
- `all_questions.json`: The raw source data (JSON).
- `scripts/update_questions_js.py`: Python script to sync `all_questions.json` -> `js/questions.js`.
- `audio/`: Sound assets for the Foreman.

---

## 🚀 How to Run (No Install)

You don't need a server. You don't need `npm`.

1. **Download** this folder.
2. **Open `index.html`** in Chrome, Safari, or Edge.
3. **Play**.

*(Note: This works because we moved the data to `js/questions.js` to avoid CORS issues with local JSON files).*

---

## 📲 How to Install (Mobile)

### **Option A: Progressive Web App (PWA)**
1. Upload this folder to a web host (GitHub Pages, Netlify, etc.).
2. Visit the URL on your phone.
3. Tap **"Share"** (iOS) or **"Menu"** (Android) -> **"Add to Home Screen"**.
4. It now looks and feels like a native app.

### **Option B: Native Android/iOS App (Capacitor)**
If you want to publish to the App Store or Play Store:

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Initialize Capacitor** (if not done):
   ```bash
   npx cap init
   ```

3. **Add Platforms**:
   ```bash
   npx cap add android
   npx cap add ios
   ```

4. **Sync & Build**:
   ```bash
   # 1. Run the Python script to ensure js/questions.js is fresh
   python scripts/update_questions_js.py

   # 2. Copy assets to native projects
   npx cap copy

   # 3. Open in Android Studio / Xcode
   npx cap open android
   # or
   npx cap open ios
   ```

---

## 🔧 Maintenance

**Adding New Questions:**
1. Edit `all_questions.json`.
2. Run `python scripts/update_questions_js.py`.
3. Commit changes.
