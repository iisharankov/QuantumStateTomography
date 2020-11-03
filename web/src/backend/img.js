async function getImg(response) {
  // Receive image from backend
  const reply = await response.json();
  const { img } = reply;
  return img;
}

export default getImg;
