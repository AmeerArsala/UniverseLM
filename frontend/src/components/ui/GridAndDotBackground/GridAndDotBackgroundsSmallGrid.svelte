<script lang="ts">
	export let showFade: boolean = true;
</script>

<div
	class="relative flex h-96 w-[50vw] items-center justify-center bg-white p-8 bg-grid-small-black/[0.2] dark:bg-black dark:bg-grid-small-white/[0.2]"
>
	<!-- Radial gradient for the container to give a faded look -->
	{#if showFade}
		<div
			class="pointer-events-none absolute inset-0 flex items-center justify-center bg-white [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)] dark:bg-black"
		></div>
	{/if}
	<slot />
</div>
