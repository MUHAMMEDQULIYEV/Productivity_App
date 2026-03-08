/**
 * Notifications / Settings component.
 */

import { api, showToast } from '../api.js';

export async function renderNotifications() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <h1 class="text-2xl font-bold mb-6">Notification Settings</h1>
    <div id="settings-loading" class="text-gray-400">Loading…</div>
    <div id="settings-form-container" class="hidden max-w-lg space-y-6"></div>`;

  const settings = await api.get('/notifications/settings');
  document.getElementById('settings-loading').classList.add('hidden');
  const container = document.getElementById('settings-form-container');
  if (!container) return;
  container.classList.remove('hidden');

  container.innerHTML = `
    <form id="settings-form" class="bg-white dark:bg-gray-800 rounded-xl shadow p-6 space-y-4">
      <h2 class="font-semibold text-lg">SMTP Configuration</h2>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm text-gray-500">SMTP Host</label>
          <input name="smtp_host" value="${settings.smtp_host || ''}" placeholder="smtp.gmail.com"
            class="w-full mt-1 border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
        </div>
        <div>
          <label class="text-sm text-gray-500">SMTP Port</label>
          <input name="smtp_port" type="number" value="${settings.smtp_port || 587}"
            class="w-full mt-1 border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
        </div>
      </div>
      <div>
        <label class="text-sm text-gray-500">SMTP Username</label>
        <input name="smtp_user" value="${settings.smtp_user || ''}" placeholder="you@gmail.com"
          class="w-full mt-1 border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
      </div>
      <div>
        <label class="text-sm text-gray-500">SMTP Password</label>
        <input name="smtp_password" type="password" placeholder="(unchanged if blank)"
          class="w-full mt-1 border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
      </div>
      <div>
        <label class="text-sm text-gray-500">Recipient Email</label>
        <input name="recipient_email" value="${settings.recipient_email || ''}" placeholder="you@example.com"
          class="w-full mt-1 border rounded-lg px-3 py-2 dark:bg-gray-700 dark:border-gray-600" />
      </div>

      <h2 class="font-semibold text-lg pt-2">Notification Preferences</h2>
      <label class="flex items-center gap-2 cursor-pointer">
        <input type="checkbox" name="notify_task_reminder" ${settings.notify_task_reminder ? 'checked' : ''} />
        Task deadline reminders (hourly check)
      </label>
      <label class="flex items-center gap-2 cursor-pointer">
        <input type="checkbox" name="notify_daily_summary" ${settings.notify_daily_summary ? 'checked' : ''} />
        Daily summary (8 AM UTC)
      </label>
      <label class="flex items-center gap-2 cursor-pointer">
        <input type="checkbox" name="notify_weekly_report" ${settings.notify_weekly_report ? 'checked' : ''} />
        Weekly report (Monday 8 AM UTC)
      </label>

      <div class="flex gap-3 pt-2">
        <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Save Settings</button>
        <button type="button" id="test-email-btn" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg hover:opacity-80">Send Test Email</button>
        <button type="button" id="daily-summary-btn" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg hover:opacity-80">Trigger Daily Summary</button>
      </div>
    </form>`;

  document.getElementById('settings-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const payload = {
      smtp_host: fd.get('smtp_host') || '',
      smtp_port: Number(fd.get('smtp_port')) || 587,
      smtp_user: fd.get('smtp_user') || '',
      smtp_password: fd.get('smtp_password') || '',
      recipient_email: fd.get('recipient_email') || '',
      notify_task_reminder: fd.get('notify_task_reminder') === 'on',
      notify_daily_summary: fd.get('notify_daily_summary') === 'on',
      notify_weekly_report: fd.get('notify_weekly_report') === 'on',
    };
    await api.post('/notifications/settings', payload);
    showToast('Settings saved', 'success');
  });

  document.getElementById('test-email-btn').addEventListener('click', async () => {
    const recipient = document.querySelector('[name="recipient_email"]').value.trim();
    if (!recipient) return showToast('Enter a recipient email first', 'error');
    await api.post('/notifications/test-email', { recipient });
    showToast('Test email sent!', 'success');
  });

  document.getElementById('daily-summary-btn').addEventListener('click', async () => {
    await api.post('/notifications/send-daily-summary', {});
    showToast('Daily summary triggered', 'success');
  });
}
