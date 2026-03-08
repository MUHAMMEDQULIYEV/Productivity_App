/**
 * App entry point — initialise router, dark mode, and render dashboard.
 */

import { route, startRouter, navigate } from './utils/router.js';
import { renderTasks } from './components/tasks.js';
import { renderNotes } from './components/notes.js';
import { renderFlashcards } from './components/flashcards.js';
import { renderLanguage } from './components/language.js';
import { renderAnalytics } from './components/analytics.js';
import { renderNotifications } from './components/notifications.js';
import { api } from './api.js';

// ── Dark mode ─────────────────────────────────────────────────────────────────
function initDarkMode() {
  const html = document.documentElement;
  const saved = localStorage.getItem('darkMode');
  if (saved === 'false') html.classList.remove('dark');
  else html.classList.add('dark');

  document.getElementById('dark-toggle')?.addEventListener('click', () => {
    const isDark = html.classList.toggle('dark');
    localStorage.setItem('darkMode', isDark);
  });
}

// ── Dashboard ─────────────────────────────────────────────────────────────────
async function renderDashboard() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    <div id="dash-loading" class="text-gray-400">Loading…</div>
    <div id="dash-content" class="hidden space-y-6"></div>`;

  try {
    const [dashboard, recs, upcoming] = await Promise.all([
      api.get('/analytics/dashboard'),
      api.get('/analytics/recommendations'),
      api.get('/tasks/upcoming'),
    ]);

    document.getElementById('dash-loading').classList.add('hidden');
    const content = document.getElementById('dash-content');
    if (!content) return;
    content.classList.remove('hidden');

    // Summary cards
    const cards = [
      { label: 'Tasks completed today', value: dashboard.tasks_completed_today, icon: '✅', color: 'bg-green-50 dark:bg-green-900' },
      { label: 'Tasks due today', value: dashboard.tasks_due_today, icon: '📅', color: 'bg-yellow-50 dark:bg-yellow-900' },
      { label: 'Vocab learned (week)', value: dashboard.vocabulary_learned_this_week, icon: '📖', color: 'bg-blue-50 dark:bg-blue-900' },
      { label: 'Flashcards due', value: dashboard.total_flashcards_due, icon: '🃏', color: 'bg-purple-50 dark:bg-purple-900' },
    ];
    content.innerHTML = `
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        ${cards.map((c) => `
          <div class="${c.color} rounded-xl shadow p-4 flex items-center gap-4">
            <span class="text-3xl">${c.icon}</span>
            <div>
              <p class="text-2xl font-bold">${c.value}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">${c.label}</p>
            </div>
          </div>`).join('')}
      </div>

      ${upcoming.length ? `
        <div>
          <h2 class="text-lg font-semibold mb-3">⏰ Upcoming Deadlines (next 24h)</h2>
          <div class="space-y-2">
            ${upcoming.map((t) => `
              <div class="bg-white dark:bg-gray-800 rounded-xl shadow px-4 py-3 flex items-center justify-between">
                <span class="font-medium">${t.title}</span>
                <span class="text-sm text-gray-400">${new Date(t.deadline).toLocaleString()}</span>
              </div>`).join('')}
          </div>
        </div>` : ''}

      <div>
        <h2 class="text-lg font-semibold mb-3">💡 Recommendations</h2>
        <div class="space-y-2">
          ${recs.map((r) => {
            const colors = { high: 'border-red-400 bg-red-50 dark:bg-red-950', medium: 'border-yellow-400 bg-yellow-50 dark:bg-yellow-950', low: 'border-green-400 bg-green-50 dark:bg-green-950' };
            return `<div class="border-l-4 rounded-r-lg px-4 py-2 text-sm ${colors[r.priority] || ''}">${r.message}</div>`;
          }).join('')}
        </div>
      </div>

      <div class="grid sm:grid-cols-3 gap-3 pt-2">
        <button onclick="navigate('/tasks')" class="px-4 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700">Go to Tasks →</button>
        <button onclick="navigate('/flashcards')" class="px-4 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700">Study Flashcards →</button>
        <button onclick="navigate('/language')" class="px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700">Extract Vocabulary →</button>
      </div>`;
  } catch (_) {
    document.getElementById('dash-loading').textContent = 'Could not load dashboard data.';
  }
}

// Expose navigate globally for inline onclick handlers in dashboard
window.navigate = navigate;

// ── Routes ────────────────────────────────────────────────────────────────────
route('/', renderDashboard);
route('/tasks', renderTasks);
route('/notes', renderNotes);
route('/flashcards', renderFlashcards);
route('/language', renderLanguage);
route('/analytics', renderAnalytics);
route('/settings', renderNotifications);

// ── Boot ──────────────────────────────────────────────────────────────────────
initDarkMode();
startRouter();
