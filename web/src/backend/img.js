async function getImg(response) {
  const reply = await response.json();
  const { img } = reply;
  return img;
}

export default getImg;
