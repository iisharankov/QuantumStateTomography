const POST_DOMAIN = 'http://127.0.0.1:5000/';

async function post(id, data) {
  return fetch(POST_DOMAIN + id, { method: 'POST', body: JSON.stringify(data) });
}

export default post;
