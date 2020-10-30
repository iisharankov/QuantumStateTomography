const POST_DOMAIN = 'http://quantumstatetomography.sharankov.com:81/';

async function post(id, data) {
  // Send POST request to backend
  return fetch(POST_DOMAIN + id, { method: 'POST', body: JSON.stringify(data) });
}

export default post;
