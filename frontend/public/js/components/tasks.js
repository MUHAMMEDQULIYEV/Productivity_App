/**
 * Tasks component — list, create, edit, delete tasks.
 */

import { api, showToast } from '../api.js';

const PRIORITIES = ['high', 'medium', 'low'];
const STATUSES = ['not_started', 'in_progress', 'completed', 'archived'];
const CATEGORIES = ['work', 'study', 'learning', 'personal'];

const PRIORITY_COLORS = {
  high: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300',
  medium: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300',
  low: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
};

function formatDate(dt) {
  if (!dt) return '—';
  return new Date(dt).toLocaleString();
}

function taskCard(task) {
  return `
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4 flex flex-col gap-2" data-task-id="${task.id}">
      <div class="flex items-start justify-between gap-2">
        <h3 class="font-semibold text-base">${escHtml(task.title)}</h3>
        <span class="text-xs px-2 py-0.5 rounded-full ${PRIORITY_COLORS[task.priority] || ''}">${task.priority}</span>
      </div>
      ${task.description ? `<p class="text-sm text-gray-500 dark:text-gray-400">${escHtml(task.description)}</p>` : ''}
      <div class="flex flex-wrap gap-2 text-xs text-gray-500 dark:text-gray-400">
        <span>📁 ${task.category}</span>
        <span>🔖 ${task.status.replace('_', ' ')}</span>
        ${task.deadline ? `<span>⏰ ${formatDate(task.deadline)}</span>` : ''}
        ${task.estimated_duration ? `<span>⏱ ${task.estimated_duration}m</span>` : ''}
      </div>
      <div class="flex gap-2 mt-1">
        <button class="btn-edit text-xs px-3 py-1 rounded bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 hover:opacity-80"
          data-id="${task.id}">Edit</button>
        <button class="btn-delete text-xs px-3 py-1 rounded bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 hover:opacity-80"
          data-id="${task.id}">Delete</button>
      </div>
    </div>`;
}

function modalHtml(task = null) {
  const t = task || {};
  return `
    <div id="task-modal" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 w-full max-w-lg">
        <h2 class="text-lg font-bold mb-4">${task ? 'Edit' : 'New'} Task</h2>
        <form id="task-form" class="space-y-3">
          <input name="title" placeholder="Title" required value="${escHtml(t.title || '')}"
            class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
          <textarea name="description" placeholder="Description (optional)" rows="3"
            class="w-full border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">${escHtml(t.description || '')}</textarea>
          <div class="grid grid-cols-2 gap-3">
            <select name="category" class="border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">
              ${CATEGORIES.map((c) => `<option value="${c}" ${t.category === c ? 'selected' : ''}>${c}</option>`).join('')}
            </select>
            <select name="priority" class="border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">
              ${PRIORITIES.map((p) => `<option value="${p}" ${t.priority === p ? 'selected' : ''}>${p}</option>`).join('')}
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <select name="status" class="border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600">
              ${STATUSES.map((s) => `<option value="${s}" ${t.status === s ? 'selected' : ''}>${s.replace(/_/g, ' ')}</option>`).join('')}
            </select>
            <input type="number" name="estimated_duration" placeholder="Est. mins" min="1"
              value="${t.estimated_duration || ''}"
              class="border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
          </div>
          <input type="datetime-local" name="deadline"
            value="${t.deadline ? new Date(t.deadline).toISOString().slice(0, 16) : ''}"
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

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export async function renderTasks() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Tasks</h1>
      <button id="new-task-btn" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">+ New Task</button>
    </div>
    <!-- Filters -->
    <div class="flex flex-wrap gap-3 mb-6">
      <select id="filter-status" class="border rounded-lg px-3 py-1.5 text-sm dark:bg-gray-800 dark:border-gray-600">
        <option value="">All statuses</option>
        ${STATUSES.map((s) => `<option value="${s}">${s.replace(/_/g, ' ')}</option>`).join('')}
      </select>
      <select id="filter-priority" class="border rounded-lg px-3 py-1.5 text-sm dark:bg-gray-800 dark:border-gray-600">
        <option value="">All priorities</option>
        ${PRIORITIES.map((p) => `<option value="${p}">${p}</option>`).join('')}
      </select>
      <select id="filter-category" class="border rounded-lg px-3 py-1.5 text-sm dark:bg-gray-800 dark:border-gray-600">
        <option value="">All categories</option>
        ${CATEGORIES.map((c) => `<option value="${c}">${c}</option>`).join('')}
      </select>
    </div>
    <div id="tasks-list" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"></div>`;

  let editingTask = null;

  const loadTasks = async () => {
    const status = document.getElementById('filter-status').value;
    const priority = document.getElementById('filter-priority').value;
    const category = document.getElementById('filter-category').value;
    const params = new URLSearchParams();
    if (status) params.set('status', status);
    if (priority) params.set('priority', priority);
    if (category) params.set('category', category);
    const qs = params.toString();
    const tasks = await api.get(`/tasks${qs ? '?' + qs : ''}`);
    const list = document.getElementById('tasks-list');
    if (!list) return;
    list.innerHTML = tasks.length
      ? tasks.map(taskCard).join('')
      : '<p class="text-gray-400 col-span-3">No tasks found.</p>';
    attachCardListeners(tasks);
  };

  const openModal = (task = null) => {
    editingTask = task;
    document.body.insertAdjacentHTML('beforeend', modalHtml(task));
    document.getElementById('modal-cancel').addEventListener('click', closeModal);
    document.getElementById('task-form').addEventListener('submit', handleSubmit);
  };

  const closeModal = () => {
    document.getElementById('task-modal')?.remove();
    editingTask = null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const payload = {
      title: fd.get('title'),
      description: fd.get('description') || null,
      category: fd.get('category'),
      priority: fd.get('priority'),
      status: fd.get('status'),
      estimated_duration: fd.get('estimated_duration') ? Number(fd.get('estimated_duration')) : null,
      deadline: fd.get('deadline') ? new Date(fd.get('deadline')).toISOString() : null,
    };
    try {
      if (editingTask) {
        await api.put(`/tasks/${editingTask.id}`, payload);
        showToast('Task updated', 'success');
      } else {
        await api.post('/tasks', payload);
        showToast('Task created', 'success');
      }
      closeModal();
      await loadTasks();
    } catch (_) { /* error shown by api */ }
  };

  const attachCardListeners = (tasks) => {
    document.querySelectorAll('.btn-edit').forEach((btn) => {
      btn.addEventListener('click', () => {
        const task = tasks.find((t) => t.id === btn.dataset.id);
        if (task) openModal(task);
      });
    });
    document.querySelectorAll('.btn-delete').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!confirm('Delete this task?')) return;
        await api.del(`/tasks/${btn.dataset.id}`);
        showToast('Task deleted');
        await loadTasks();
      });
    });
  };

  document.getElementById('new-task-btn').addEventListener('click', () => openModal());
  ['filter-status', 'filter-priority', 'filter-category'].forEach((id) => {
    document.getElementById(id).addEventListener('change', loadTasks);
  });

  await loadTasks();
}
