/**
 * Analytics component — dashboard charts and recommendations.
 */

import { api } from '../api.js';

let chartInstances = [];

function destroyCharts() {
  chartInstances.forEach((c) => c.destroy());
  chartInstances = [];
}

export async function renderAnalytics() {
  destroyCharts();
  const app = document.getElementById('app');
  app.innerHTML = `
    <h1 class="text-2xl font-bold mb-6">Analytics</h1>
    <div id="analytics-loading" class="text-gray-400">Loading…</div>
    <div id="analytics-content" class="hidden space-y-8">
      <!-- Summary cards -->
      <div id="summary-cards" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"></div>

      <!-- Charts row -->
      <div class="grid gap-6 lg:grid-cols-2">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
          <h2 class="font-semibold mb-3">Tasks by Category</h2>
          <canvas id="chart-category"></canvas>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
          <h2 class="font-semibold mb-3">Task Status Distribution</h2>
          <canvas id="chart-status"></canvas>
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
        <h2 class="font-semibold mb-3">Vocabulary Growth (learned by date)</h2>
        <canvas id="chart-vocab"></canvas>
      </div>

      <!-- Recommendations -->
      <div>
        <h2 class="text-lg font-semibold mb-3">Recommendations</h2>
        <div id="recommendations" class="space-y-2"></div>
      </div>
    </div>`;

  const [dashboard, productivity, language, recs] = await Promise.all([
    api.get('/analytics/dashboard'),
    api.get('/analytics/productivity'),
    api.get('/analytics/language'),
    api.get('/analytics/recommendations'),
  ]);

  document.getElementById('analytics-loading').classList.add('hidden');
  document.getElementById('analytics-content').classList.remove('hidden');

  // Summary cards
  const summaryCards = [
    { label: 'Tasks completed today', value: dashboard.tasks_completed_today, icon: '✅' },
    { label: 'Tasks due today', value: dashboard.tasks_due_today, icon: '📅' },
    { label: 'Vocabulary learned (week)', value: dashboard.vocabulary_learned_this_week, icon: '📖' },
    { label: 'Flashcard accuracy', value: `${dashboard.flashcard_accuracy_this_week}%`, icon: '🎯' },
  ];
  document.getElementById('summary-cards').innerHTML = summaryCards
    .map(
      (c) => `
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4 flex items-center gap-4">
          <span class="text-3xl">${c.icon}</span>
          <div>
            <p class="text-2xl font-bold">${c.value}</p>
            <p class="text-sm text-gray-400">${c.label}</p>
          </div>
        </div>`
    )
    .join('');

  // Category bar chart
  const catData = productivity.category_breakdown || {};
  const catLabels = Object.keys(catData);
  const catCompleted = catLabels.map((k) => catData[k].completed);
  const catTotal = catLabels.map((k) => catData[k].total);
  if (catLabels.length) {
    chartInstances.push(
      new Chart(document.getElementById('chart-category'), {
        type: 'bar',
        data: {
          labels: catLabels,
          datasets: [
            { label: 'Completed', data: catCompleted, backgroundColor: 'rgba(99,102,241,0.7)' },
            { label: 'Total', data: catTotal, backgroundColor: 'rgba(203,213,225,0.5)' },
          ],
        },
        options: { responsive: true, plugins: { legend: { position: 'top' } } },
      })
    );
  }

  // Status pie chart (derive from productivity data)
  const statusPieLabels = ['Completed', 'Remaining'];
  const statusPieData = [
    productivity.completed_tasks || 0,
    (productivity.total_tasks || 0) - (productivity.completed_tasks || 0),
  ];
  chartInstances.push(
    new Chart(document.getElementById('chart-status'), {
      type: 'pie',
      data: {
        labels: statusPieLabels,
        datasets: [
          {
            data: statusPieData,
            backgroundColor: ['rgba(34,197,94,0.7)', 'rgba(203,213,225,0.5)'],
          },
        ],
      },
      options: { responsive: true },
    })
  );

  // Vocabulary line chart
  const vocabByDate = language.words_by_date || {};
  const vocabLabels = Object.keys(vocabByDate).sort();
  const vocabData = vocabLabels.map((d) => vocabByDate[d]);
  chartInstances.push(
    new Chart(document.getElementById('chart-vocab'), {
      type: 'line',
      data: {
        labels: vocabLabels.length ? vocabLabels : ['No data'],
        datasets: [
          {
            label: 'Words learned',
            data: vocabData.length ? vocabData : [0],
            borderColor: 'rgba(99,102,241,0.8)',
            backgroundColor: 'rgba(99,102,241,0.15)',
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: { responsive: true },
    })
  );

  // Recommendations
  const priorityColors = { high: 'bg-red-50 dark:bg-red-900 border-red-300', medium: 'bg-yellow-50 dark:bg-yellow-900 border-yellow-300', low: 'bg-green-50 dark:bg-green-900 border-green-300' };
  document.getElementById('recommendations').innerHTML = recs
    .map(
      (r) => `
        <div class="border rounded-lg p-3 text-sm ${priorityColors[r.priority] || ''}">
          ${r.message}
        </div>`
    )
    .join('');
}
