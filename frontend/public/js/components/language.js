/**
 * Language Learning component — YouTube extraction, file upload, vocabulary table.
 */

import { api, showToast } from '../api.js';

function escHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function wordRow(item, idx) {
  return `
    <tr class="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750">
      <td class="px-3 py-2"><input type="checkbox" class="word-check" data-idx="${idx}" /></td>
      <td class="px-3 py-2 font-medium">${escHtml(item.word)}</td>
      <td class="px-3 py-2 text-gray-400">${escHtml(item.pos || '—')}</td>
      <td class="px-3 py-2 text-right tabular-nums">${item.frequency}</td>
    </tr>`;
}

export async function renderLanguage() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <h1 class="text-2xl font-bold mb-6">Language Learning</h1>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6">
      <button class="tab-btn active px-4 py-2 rounded-lg bg-indigo-600 text-white" data-tab="youtube">YouTube URL</button>
      <button class="tab-btn px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:opacity-80" data-tab="upload">File Upload</button>
      <button class="tab-btn px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:opacity-80" data-tab="text">Paste Text</button>
      <button class="tab-btn px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:opacity-80" data-tab="saved">Saved Vocabulary</button>
    </div>

    <!-- Tab panels -->
    <div id="tab-youtube" class="tab-panel space-y-3">
      <input id="yt-url" type="url" placeholder="https://www.youtube.com/watch?v=..."
        class="w-full border rounded-lg px-3 py-2 dark:bg-gray-800 dark:border-gray-600" />
      <button id="yt-extract-btn" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">Extract from YouTube</button>
    </div>

    <div id="tab-upload" class="tab-panel hidden space-y-3">
      <input id="file-input" type="file" accept=".srt,.txt"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-50 file:text-indigo-700 dark:file:bg-indigo-900 dark:file:text-indigo-300" />
      <button id="file-extract-btn" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Extract from File</button>
    </div>

    <div id="tab-text" class="tab-panel hidden space-y-3">
      <textarea id="raw-text" rows="8" placeholder="Paste text here…"
        class="w-full border rounded-lg px-3 py-2 font-mono text-sm dark:bg-gray-800 dark:border-gray-600"></textarea>
      <button id="text-extract-btn" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Extract Words</button>
    </div>

    <div id="tab-saved" class="tab-panel hidden">
      <div id="saved-vocab-list"></div>
    </div>

    <!-- Results -->
    <div id="word-results" class="mt-6 hidden">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-lg font-semibold">Extracted Words <span id="word-count" class="text-gray-400 text-sm"></span></h2>
        <button id="save-selected-btn" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">💾 Save Selected to Vocabulary</button>
      </div>
      <div class="overflow-x-auto rounded-xl shadow">
        <table class="w-full text-sm bg-white dark:bg-gray-800">
          <thead class="bg-gray-50 dark:bg-gray-700 text-left">
            <tr>
              <th class="px-3 py-2"><input type="checkbox" id="select-all" /></th>
              <th class="px-3 py-2">Word</th>
              <th class="px-3 py-2">POS</th>
              <th class="px-3 py-2 text-right">Frequency</th>
            </tr>
          </thead>
          <tbody id="word-table-body"></tbody>
        </table>
      </div>
    </div>`;

  let extractedWords = [];
  let currentSourceUrl = null;

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => {
        b.classList.remove('active', 'bg-indigo-600', 'text-white');
        b.classList.add('bg-gray-100', 'dark:bg-gray-700');
      });
      btn.classList.add('active', 'bg-indigo-600', 'text-white');
      btn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
      document.querySelectorAll('.tab-panel').forEach((p) => p.classList.add('hidden'));
      document.getElementById(`tab-${btn.dataset.tab}`)?.classList.remove('hidden');
      if (btn.dataset.tab === 'saved') loadSavedVocab();
    });
  });

  const showResults = (words, sourceUrl = null) => {
    extractedWords = words;
    currentSourceUrl = sourceUrl;
    const results = document.getElementById('word-results');
    if (!results) return;
    results.classList.remove('hidden');
    document.getElementById('word-count').textContent = `(${words.length} words)`;
    document.getElementById('word-table-body').innerHTML = words.map(wordRow).join('');
    document.getElementById('select-all').addEventListener('change', (e) => {
      document.querySelectorAll('.word-check').forEach((c) => { c.checked = e.target.checked; });
    });
  };

  // YouTube extraction
  document.getElementById('yt-extract-btn').addEventListener('click', async () => {
    const url = document.getElementById('yt-url').value.trim();
    if (!url) return showToast('Enter a YouTube URL', 'error');
    const words = await api.post('/language/extract-youtube', { url });
    showResults(words, url);
  });

  // File extraction
  document.getElementById('file-extract-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('file-input');
    if (!fileInput.files.length) return showToast('Select a file first', 'error');
    const fd = new FormData();
    fd.append('file', fileInput.files[0]);
    const words = await api.upload('/language/extract-upload', fd);
    showResults(words);
  });

  // Text extraction
  document.getElementById('text-extract-btn').addEventListener('click', async () => {
    const text = document.getElementById('raw-text').value.trim();
    if (!text) return showToast('Paste some text first', 'error');
    const words = await api.post('/language/extract-text', { text });
    showResults(words);
  });

  // Save selected words
  document.getElementById('save-selected-btn').addEventListener('click', async () => {
    const checked = [...document.querySelectorAll('.word-check:checked')];
    if (!checked.length) return showToast('Select at least one word', 'error');
    const items = checked
      .map((c) => extractedWords[Number(c.dataset.idx)])
      .filter((item) => item !== undefined);
    if (!items.length) return showToast('No valid words selected', 'error');
    await api.post('/language/vocabulary/save', {
      items,
      language: 'english',
      source_url: currentSourceUrl,
    });
    showToast(`Saved ${items.length} word(s)`, 'success');
  });

  const loadSavedVocab = async () => {
    const words = await api.get('/language/vocabulary');
    const container = document.getElementById('saved-vocab-list');
    if (!container) return;
    if (!words.length) {
      container.innerHTML = '<p class="text-gray-400">No saved vocabulary yet.</p>';
      return;
    }
    container.innerHTML = `
      <div class="overflow-x-auto rounded-xl shadow mt-2">
        <table class="w-full text-sm bg-white dark:bg-gray-800">
          <thead class="bg-gray-50 dark:bg-gray-700 text-left">
            <tr>
              <th class="px-3 py-2">Word</th>
              <th class="px-3 py-2">Language</th>
              <th class="px-3 py-2">Frequency</th>
              <th class="px-3 py-2">Learned</th>
              <th class="px-3 py-2"></th>
            </tr>
          </thead>
          <tbody>
            ${words.map((w) => `
              <tr class="border-b border-gray-100 dark:border-gray-700">
                <td class="px-3 py-2 font-medium">${escHtml(w.word)}</td>
                <td class="px-3 py-2 text-gray-400">${w.language}</td>
                <td class="px-3 py-2">${w.frequency_count}</td>
                <td class="px-3 py-2">${w.learned ? '✅' : '—'}</td>
                <td class="px-3 py-2">
                  ${!w.learned ? `<button class="btn-mark-learned text-xs px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:opacity-80" data-id="${w.id}">Mark learned</button>` : ''}
                </td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>`;

    document.querySelectorAll('.btn-mark-learned').forEach((btn) => {
      btn.addEventListener('click', async () => {
        await api.put(`/language/vocabulary/${btn.dataset.id}/mark-learned`, {});
        showToast('Marked as learned', 'success');
        await loadSavedVocab();
      });
    });
  };
}
