// Use relative URLs - Vite proxy will handle routing in development
// In production, these should be served from the same origin or configured separately
async function post(id, data) {
  // Send POST request to backend
  return fetch('/' + id, { method: 'POST', body: JSON.stringify(data) });
}

export default post;
