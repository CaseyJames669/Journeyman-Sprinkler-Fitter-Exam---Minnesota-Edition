# MN Sprinkler Quiz — PWA + Capacitor Scaffold

This repository contains a browser-based MN Sprinkler Journeyman quiz. The project is set up as a Progressive Web App (PWA) and includes scaffolding to wrap the app with Capacitor for native Android/iOS distribution.

What I added
- `package.json` — basic scripts for serving and Capacitor commands.
- `capacitor.config.json` — config for Capacitor when you run `npx cap add`.
- `manifest.json` — PWA manifest to make the app installable.
- `sw.js` — basic service worker to cache key assets for offline use.
- `scripts/validate_datasets.py` — simple validator for `datasets/*.json`.

Goals & next steps to publish to stores
1. Test PWA locally: `npx serve -s .` or `npm run start`.
2. Verify offline behavior by opening `study.html` in Chrome, install PWA, and test offline.
3. If you want native apps: install Capacitor and add platforms:

```bash
# from repo root
npm install
# install Capacitor runtime
npx cap init
# then add platform (example android)
npx cap add android
# copy web assets and open Android Studio
npx cap copy
npx cap open android
```

4. In Android Studio / Xcode, configure app id, signing, icons, and build.

Notes
- Do NOT add copyrighted audio files unless you own the rights. Replace with royalty-free clips or rely on the WebAudio synth fallback.
- Consider consolidating inline JS in `study.html` into `js/` files and using a small bundler for cleaner builds.

Validation
- Run dataset validation: `npm run validate:data` (requires Python 3).

If you want, I can continue and:
- Move inline app logic into `js/app.js` and use a minimal build step.
- Add proper icons/splash images and adapt `manifest.json` entries.
- Create a small CI script to validate datasets on push.
