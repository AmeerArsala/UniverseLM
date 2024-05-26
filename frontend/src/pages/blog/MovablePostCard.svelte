<script lang="ts">
  import { Motion, MotionValue, useTransform, useSpring, useViewportScroll } from 'svelte-motion';

  export let translate: MotionValue<number>;
</script>

<Motion
  let:motion
  style={{
    x: translate
  }}
  whileHover={{
    y: -20
  }}
>
  <div use:motion class="group/product relative w-[30rem] flex-shrink-0">
    <slot />
  </div>
</Motion>
