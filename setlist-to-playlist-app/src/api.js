const API_BASE = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE) {
  console.warn("VITE_API_BASE_URL is not defined");
}

export function apiFetch(path, options = {}) {
  return fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
}