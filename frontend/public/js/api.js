/**
 * Fetch wrapper for all API calls.
 * Base URL is resolved from the current origin so the frontend works
 * both when served by Nginx (which proxies /api → backend) and locally.
 */

const BASE_URL = '/api';

/** Show a brief toast notification. */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const colors = {
    info: 'bg-blue-500',
    success: 'bg-green-500',
    error: 'bg-red-500',
  };
  const toast = document.createElement('div');
  toast.className = `${colors[type] || colors.info} text-white px-4 py-2 rounded-lg shadow-lg text-sm transition-opacity`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

async function request(method, path, body = null, isFormData = false, opts = {}) {
  const options = {
    method,
    headers: isFormData ? {} : { 'Content-Type': 'application/json' },
  };
  if (body) {
    options.body = isFormData ? body : JSON.stringify(body);
  }

  const res = await fetch(`${BASE_URL}${path}`, options);

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const err = await res.json();
      detail = err.detail || detail;
    } catch (_) { /* ignore */ }
    if (!opts.silent) showToast(detail, 'error');
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  get: (path, opts) => request('GET', path, null, false, opts),
  post: (path, body, opts) => request('POST', path, body, false, opts),
  put: (path, body, opts) => request('PUT', path, body, false, opts),
  del: (path, opts) => request('DELETE', path, null, false, opts),
  upload: (path, formData, opts) => request('POST', path, formData, true, opts),
};

export { showToast };
