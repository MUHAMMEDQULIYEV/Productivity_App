/**
 * Client-side hash router.
 * Maps hash paths like #/tasks to render functions.
 */

const _routes = {};

/**
 * Register a route.
 * @param {string} path - e.g. '/tasks'
 * @param {function(): Promise<void>} handler - async render function
 */
export function route(path, handler) {
  _routes[path] = handler;
}

/** Navigate programmatically to a hash path. */
export function navigate(path) {
  window.location.hash = `#${path}`;
}

/** Return the current hash path without the '#'. */
function currentPath() {
  const hash = window.location.hash || '#/';
  return hash.slice(1) || '/';
}

/** Start the router — listen for hash changes. */
export function startRouter() {
  const dispatch = async () => {
    const path = currentPath();
    const handler = _routes[path] || _routes['/'];

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach((el) => {
      const r = el.dataset.route;
      el.classList.toggle('active', r === path);
    });

    if (handler) {
      await handler();
    } else {
      document.getElementById('app').innerHTML =
        '<p class="text-gray-500">Page not found.</p>';
    }
  };

  window.addEventListener('hashchange', dispatch);
  dispatch(); // render on first load
}
