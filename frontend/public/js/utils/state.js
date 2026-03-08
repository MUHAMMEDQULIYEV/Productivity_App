/**
 * Simple reactive state store.
 * Components can subscribe to state changes.
 */

const _state = {};
const _subscribers = {};

/**
 * Get a state value.
 * @param {string} key
 * @returns {*}
 */
export function getState(key) {
  return _state[key];
}

/**
 * Set a state value and notify subscribers.
 * @param {string} key
 * @param {*} value
 */
export function setState(key, value) {
  _state[key] = value;
  (_subscribers[key] || []).forEach((fn) => fn(value));
}

/**
 * Subscribe to state changes for a key.
 * @param {string} key
 * @param {function(*): void} fn
 * @returns {function(): void} Unsubscribe function
 */
export function subscribe(key, fn) {
  if (!_subscribers[key]) _subscribers[key] = [];
  _subscribers[key].push(fn);
  return () => {
    _subscribers[key] = _subscribers[key].filter((f) => f !== fn);
  };
}
