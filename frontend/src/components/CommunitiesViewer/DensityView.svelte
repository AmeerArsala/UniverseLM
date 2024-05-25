<script lang="ts">
  import { calculateColor, type Color } from "./density";
  import { Indicator, Badge } from "flowbite-svelte";

  export let density: number = 0.0;

  // Calculate the color and label for it
  let color: Color = calculateColor(density);

  // Calculate label
  let label: string = "Average";

  if (density >= 1.5) {
    label = "Rich";
  } else if (density <= -1.5) {
    label = "Barren";
  } else if (density <= -1) {
    label = "Small";
  } else if (density >= 1) {
    label = "Moderate";
  }

  let badgeColor: Color = {
    hue: color.hue,
    saturation: Math.floor(color.saturation * 0.5),
    luminosity: Math.floor(color.luminosity * 0.5)
  };

  let textColor: Color = {
    hue: color.hue,
    saturation: color.saturation,
    luminosity: color.luminosity + 35
  };

  function colorToString(c: Color): string {
    return `hsl(${c.hue},${c.saturation}%,${c.luminosity}%)`;
  }

  function colorAToString(c: Color, a: number): string {
    return `hsla(${c.hue},${c.saturation}%,${c.luminosity}%,${a})`;
  }

  const badgeStyle: string = `background-color: ${colorToString(badgeColor)}; color: ${colorToString(textColor)};`;
  const indicatorStyle: string = `background-color: ${colorAToString(color, 1)};`;
</script>

<div class="flex flex-row items-center ">

  <div style={badgeStyle} class="px-2.5 py-0.5 rounded-full flex flex-row items-center max-w-[6rem] text-center justify-center">
    {label}
  </div>
</div>


