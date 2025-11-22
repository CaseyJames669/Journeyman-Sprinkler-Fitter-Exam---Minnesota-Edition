const CACHE_NAME = 'mnsprinkler-v1';
const ASSETS = [
  './study.html',
  './index.html',
  './manifest.json',
  './css/style.css',
  './js/game.js',
  './js/questions.js'
];
// Add images and audio to cache (optional: remove large audio if size is a concern)
const ADDITIONAL = [
  './assets/foreman-success.jpg',
  './assets/foreman-neutral.jpg',
  './assets/foreman-loading.jpg',
  './assets/foreman-fail.jpg',
  './audio/never-never-never-never-ever-ever-ever-ever.mp3',
  './audio/it-s-a-shame.mp3',
  './audio/do-your-parents-know-you-don-t-know-that.mp3',
  './audio/beta-baby.mp3',
  './audio/amazing-i-have-no-anger.mp3',
  './audio/absolutely-perfect.mp3'
];

const ALL_ASSETS = ASSETS.concat(ADDITIONAL);

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ALL_ASSETS))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => resp || fetch(event.request))
  );
});
