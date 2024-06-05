<script lang="ts">
	export let showFade: boolean = true;
</script>

<div
	class="relative flex w-[60vw] h-64 items-center bg-white bg-grid-black/[0.2] dark:bg-black dark:bg-grid-white/[0.2] ml-auto mr-auto"
>
	<!-- Radial gradient for the container to give a faded look -->
  {#if showFade}
		<div
			class="pointer-events-none absolute inset-0 bg-white rounded-lg [mask-image:radial-gradient(ellipse_at_center,transparent_5%,black)] dark:bg-black"
		></div>
	{/if}
	<slot />
</div>
