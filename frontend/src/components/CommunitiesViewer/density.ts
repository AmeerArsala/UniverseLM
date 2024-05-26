export interface Color {
  hue: number;
  saturation: number;
  luminosity: number;
};

export function calculateColor(density: number): Color {
  // Normalize the value to a range: [-1.51, 1.51]
  let maxVal = 1.51;

  let val = density;
  //let normalized_val = Math.min(Math.max(-maxVal, density), maxVal);

  let minHue = 0;
  let maxHue = 116;

  // Start at yellow
  let h = (minHue + maxHue) / 2;
  let s = 100;
  let l = 50;

  val = (val + maxVal) / (maxVal + maxVal); // now it's in [0, 1]
  h = minHue + (val * (maxHue - minHue));

  return {hue: h, saturation: s, luminosity: l};
}
