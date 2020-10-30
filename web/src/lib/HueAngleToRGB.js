// Used to generate colours dynamically

export default function HueAngleToRGB(hueAngle) {
  //Step 1
  var saturation = 1;
  var luminance = 1;

  //Step 2
  var temporary_1 = luminance * (1 + saturation);

  //Step 3
  var temporary_2 = 2 * luminance - temporary_1;

  //Step 4
  var Hue = hueAngle / 360;

  //Step 5
  var temporary_R = Hue + 1/3;
  var temporary_G = Hue;
  var temporary_B = Hue - 1/3;

  if(temporary_R < 0){
    temporary_R += 1;
  } if (temporary_G < 0) {
    temporary_G += 1;
  } if (temporary_B < 0) {
    temporary_B += 1;
  } if (temporary_R > 1) {
    temporary_R -= 1;
  } if (temporary_G > 1) {
    temporary_G -= 1;
  } if (temporary_B > 1) {
    temporary_B -= 1;
  }

  //Step 6
  var Red = useCorrectFormula(temporary_R, temporary_1, temporary_2);
  var Green = useCorrectFormula(temporary_G, temporary_1, temporary_2);
  var Blue = useCorrectFormula(temporary_B, temporary_1, temporary_2);

  //Step 7
  Red = Math.round(Red * 255 / 2);
  Green = Math.round(Green * 255 / 2);
  Blue = Math.round(Blue * 255 / 2);

  return rgbToHex(Red, Green, Blue);
}

// http://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

// temporary_RGB may be temporary_R, temporary_G, or temporary_B
function useCorrectFormula(temporary_RGB, temporary_1, temporary_2) {
  if (6 * temporary_RGB < 1) {
    return temporary_2 + (temporary_1 - temporary_2) * 6 * temporary_RGB;
  } else if (2 * temporary_RGB < 1) {
    return temporary_1;
  } else if (3 * temporary_RGB < 2) {
    return temporary_2 + (temporary_1 - temporary_2) * (2/3 - temporary_RGB) * 6;
  } else {
    return temporary_2;
  }
}
