<script lang="ts">
	import { Dialog as SheetPrimitive } from "bits-ui";
	import { fade } from "svelte/transition";
	import { cn } from "$lib/utils.js";

	type $$Props = SheetPrimitive.OverlayProps;

	let className: $$Props["class"] = undefined;
	export let transition: $$Props["transition"] = fade;
	export let transitionConfig: $$Props["transitionConfig"] = {
		duration: 150,
	};
	export { className as class };
</script>

<!-- I took out the background blur of backdrop-blur-sm -->
<SheetPrimitive.Overlay
	{transition}
	{transitionConfig}
	class={cn("fixed inset-0 z-50 bg-background/80", className)}
	{...$$restProps}
/>
