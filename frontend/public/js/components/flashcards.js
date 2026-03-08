/**
 * Flashcards component — deck management and study mode.
 */

import { api, showToast } from '../api.js';

function escHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function deckCard(deck) {
  return `
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4 flex flex-col gap-2">
      <div class="flex items-center justify-between">
        <h3 class="font-semibold">${escHtml(deck.name)}</h3>
        <span class="text-xs bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded-full">${deck.language}</span>
      </div>
      <p class="text-sm text-gray-400">${deck.card_count} card${deck.card_count !== 1 ? 's' : ''} · ${deck.source_type}</p>
      <div class="flex gap-2 mt-1">
        <button class="btn-study flex-1 text-sm px-3 py-1.5 rounded bg-indigo-600 text-white hover:bg-indigo-700" data-id="${deck.id}" data-name="${escHtml(deck.name)}">Study</button>
        <button class="btn-delete-deck text-sm px-3 py-1.5 rounded bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 hover:opacity-80" data-id="${deck.id}">Delete</button>
      </div>
    </div>`;
}

function deckModalHtml() {
  return `
    <div id="deck-modal" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">New Deck</h2>
        <form id="deck-form" class="space-y-3">
          <input name="name" placeholder="Deck name" required
            class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
          <select name="language" class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">
            <option value="english">English</option>
            <option value="korean">Korean</option>
          </select>
          <select name="source_type" class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">
            <option value="manual">Manual</option>
            <option value="youtube">YouTube</option>
            <option value="upload">Upload</option>
          </select>
          <div class="flex gap-3 justify-end pt-2">
            <button type="button" id="deck-modal-cancel" class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:opacity-80">Cancel</button>
            <button type="submit" class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">Create</button>
          </div>
        </form>
      </div>
    </div>`;
}

async function renderStudyMode(deckId, deckName) {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="flex items-center gap-4 mb-6">
      <button id="back-to-decks" class="text-indigo-500 hover:underline">← Back to decks</button>
      <h1 class="text-2xl font-bold">Studying: ${escHtml(deckName)}</h1>
    </div>
    <div id="study-area" class="max-w-xl mx-auto"></div>`;

  document.getElementById('back-to-decks').addEventListener('click', renderFlashcards);

  const cards = await api.get(`/cards/review/${deckId}`);
  const studyArea = document.getElementById('study-area');
  if (!studyArea) return;

  if (!cards.length) {
    studyArea.innerHTML = '<div class="text-center text-gray-400 py-20 text-lg">🎉 No cards due for review!</div>';
    return;
  }

  let index = 0;

  const renderCard = () => {
    if (index >= cards.length) {
      studyArea.innerHTML = '<div class="text-center text-gray-400 py-20 text-lg">✅ Session complete!</div>';
      return;
    }
    const card = cards[index];
    studyArea.innerHTML = `
      <div class="flip-card" id="flip-card">
        <div class="flip-card-inner">
          <div class="flip-card-front bg-indigo-50 dark:bg-indigo-900 shadow-lg">
            <p class="text-2xl font-bold">${escHtml(card.front)}</p>
          </div>
          <div class="flip-card-back bg-emerald-50 dark:bg-emerald-900 shadow-lg">
            <p class="text-xl">${escHtml(card.back)}</p>
          </div>
        </div>
      </div>
      <p class="text-center text-sm text-gray-400 mt-3">Click card to flip</p>
      <div id="quality-btns" class="hidden mt-6 flex justify-center gap-3 flex-wrap">
        <button class="q-btn px-4 py-2 rounded-lg bg-red-500 text-white hover:opacity-80" data-q="0">Again (0)</button>
        <button class="q-btn px-4 py-2 rounded-lg bg-orange-500 text-white hover:opacity-80" data-q="2">Hard (2)</button>
        <button class="q-btn px-4 py-2 rounded-lg bg-green-500 text-white hover:opacity-80" data-q="4">Good (4)</button>
        <button class="q-btn px-4 py-2 rounded-lg bg-blue-500 text-white hover:opacity-80" data-q="5">Easy (5)</button>
      </div>
      <p class="text-center text-xs text-gray-400 mt-2">${index + 1} / ${cards.length}</p>`;

    document.getElementById('flip-card').addEventListener('click', () => {
      document.getElementById('flip-card').classList.toggle('flipped');
      document.getElementById('quality-btns').classList.remove('hidden');
    });

    document.querySelectorAll('.q-btn').forEach((btn) => {
      btn.addEventListener('click', async () => {
        await api.put(`/cards/${card.id}/review`, { quality: Number(btn.dataset.q) });
        index++;
        renderCard();
      });
    });
  };

  renderCard();
}

export async function renderFlashcards() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Flashcard Decks</h1>
      <button id="new-deck-btn" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">+ New Deck</button>
    </div>
    <div id="decks-list" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"></div>`;

  const loadDecks = async () => {
    const decks = await api.get('/decks');
    const list = document.getElementById('decks-list');
    if (!list) return;
    list.innerHTML = decks.length
      ? decks.map(deckCard).join('')
      : '<p class="text-gray-400 col-span-3">No decks yet. Create one!</p>';

    document.querySelectorAll('.btn-study').forEach((btn) => {
      btn.addEventListener('click', () => renderStudyMode(btn.dataset.id, btn.dataset.name));
    });
    document.querySelectorAll('.btn-delete-deck').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm('Delete this deck and all its cards?')) return;
        await api.del(`/decks/${btn.dataset.id}`);
        showToast('Deck deleted');
        await loadDecks();
      });
    });
  };

  document.getElementById('new-deck-btn').addEventListener('click', () => {
    document.body.insertAdjacentHTML('beforeend', deckModalHtml());
    document.getElementById('deck-modal-cancel').addEventListener('click', () =>
      document.getElementById('deck-modal')?.remove()
    );
    document.getElementById('deck-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.post('/decks', {
        name: fd.get('name'),
        language: fd.get('language'),
        source_type: fd.get('source_type'),
      });
      document.getElementById('deck-modal')?.remove();
      showToast('Deck created', 'success');
      await loadDecks();
    });
  });

  await loadDecks();
}
