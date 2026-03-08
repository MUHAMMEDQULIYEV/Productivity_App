/**
 * Notes component — list, create, edit, delete, search notes.
 */

import { api, showToast } from '../api.js';

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function noteCard(note) {
  const tags = (note.tags || []).map((t) => `<span class="text-xs bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 px-2 py-0.5 rounded-full">${escHtml(t)}</span>`).join(' ');
  return `
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4 flex flex-col gap-2" data-note-id="${note.id}">
      <h3 class="font-semibold">${escHtml(note.title)}</h3>
      <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-3">${escHtml(note.content || '')}</p>
      <div class="flex flex-wrap gap-1">${tags}</div>
      <div class="flex gap-2 mt-1">
        <button class="btn-edit text-xs px-3 py-1 rounded bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 hover:opacity-80" data-id="${note.id}">Edit</button>
        <button class="btn-delete text-xs px-3 py-1 rounded bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 hover:opacity-80" data-id="${note.id}">Delete</button>
      </div>
    </div>`;
}

function modalHtml(note = null) {
  const n = note || {};
  return `
    <div id="note-modal" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 w-full max-w-lg">
        <h2 class="text-lg font-bold mb-4">${note ? 'Edit' : 'New'} Note</h2>
        <form id="note-form" class="space-y-3">
          <input name="title" placeholder="Title" required value="${escHtml(n.title || '')}"
            class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
          <textarea name="content" placeholder="Content…" rows="8"
            class="w-full border rounded-lg px-3 py-2 font-mono text-sm dark:bg-gray-700 dark:border-gray-600">${escHtml(n.content || '')}</textarea>
          <input name="tags" placeholder="Tags (comma-separated)"
            value="${escHtml((n.tags || []).join(', '))}"
            class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
          <div class="flex gap-3 justify-end pt-2">
            <button type="button" id="modal-cancel"
              class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:opacity-80">Cancel</button>
            <button type="submit"
              class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">Save</button>
          </div>
        </form>
      </div>
    </div>`;
}

export async function renderNotes() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Notes</h1>
      <button id="new-note-btn" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">+ New Note</button>
    </div>
    <div class="flex gap-3 mb-6">
      <input id="search-input" type="search" placeholder="Search notes…"
        class="flex-1 border rounded-lg px-3 py-2 dark:bg-gray-800 dark:border-gray-600" />
      <input id="tag-filter" type="text" placeholder="Filter by tag"
        class="border rounded-lg px-3 py-2 dark:bg-gray-800 dark:border-gray-600" />
    </div>
    <div id="notes-list" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"></div>`;

  let editingNote = null;

  const loadNotes = async (q = '', tag = '') => {
    let notes;
    if (q) {
      notes = await api.get(`/notes/search?q=${encodeURIComponent(q)}`);
    } else {
      const qs = tag ? `?tag=${encodeURIComponent(tag)}` : '';
      notes = await api.get(`/notes${qs}`);
    }
    const list = document.getElementById('notes-list');
    if (!list) return;
    list.innerHTML = notes.length
      ? notes.map(noteCard).join('')
      : '<p class="text-gray-400 col-span-3">No notes found.</p>';
    attachCardListeners(notes);
  };

  const openModal = (note = null) => {
    editingNote = note;
    document.body.insertAdjacentHTML('beforeend', modalHtml(note));
    document.getElementById('modal-cancel').addEventListener('click', closeModal);
    document.getElementById('note-form').addEventListener('submit', handleSubmit);
  };

  const closeModal = () => {
    document.getElementById('note-modal')?.remove();
    editingNote = null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const rawTags = fd.get('tags') || '';
    const tags = rawTags.split(',').map((t) => t.trim()).filter(Boolean);
    const payload = { title: fd.get('title'), content: fd.get('content') || '', tags };
    try {
      if (editingNote) {
        await api.put(`/notes/${editingNote.id}`, payload);
        showToast('Note updated', 'success');
      } else {
        await api.post('/notes', payload);
        showToast('Note created', 'success');
      }
      closeModal();
      await loadNotes();
    } catch (_) { /* error shown by api */ }
  };

  const attachCardListeners = (notes) => {
    document.querySelectorAll('.btn-edit').forEach((btn) => {
      btn.addEventListener('click', () => {
        const note = notes.find((n) => n.id === btn.dataset.id);
        if (note) openModal(note);
      });
    });
    document.querySelectorAll('.btn-delete').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm('Delete this note?')) return;
        await api.del(`/notes/${btn.dataset.id}`);
        showToast('Note deleted');
        await loadNotes();
      });
    });
  };

  document.getElementById('new-note-btn').addEventListener('click', () => openModal());

  let searchTimeout;
  document.getElementById('search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadNotes(e.target.value, ''), 300);
  });
  document.getElementById('tag-filter').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadNotes('', e.target.value), 300);
  });

  await loadNotes();
}
