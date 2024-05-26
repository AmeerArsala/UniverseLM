<script lang="ts">
	import { ScrollArea as ScrollAreaPrimitive } from "bits-ui";
	import { Scrollbar } from "./index.js";
	import { cn } from "$lib/utils.js";

	type $$Props = ScrollAreaPrimitive.Props & {
		orientation?: "vertical" | "horizontal" | "both";
		scrollbarXClasses?: string;
		scrollbarYClasses?: string;
	};

	let className: $$Props["class"] = undefined;
	export { className as class };
	export let orientation = "vertical";
	export let scrollbarXClasses: string = "";
	export let scrollbarYClasses: string = "";

  export let showScrollbar: boolean = true;

  let scrollbarClass: string = "bg-border";
  if (!showScrollbar) {
    scrollbarClass = "bg-transparent";
  }
</script>

<ScrollAreaPrimitive.Root {...$$restProps} class={cn("relative overflow-hidden", className)}>
	<ScrollAreaPrimitive.Viewport class="h-full w-full rounded-[inherit]">
		<ScrollAreaPrimitive.Content>
			<slot />
		</ScrollAreaPrimitive.Content>
	</ScrollAreaPrimitive.Viewport>
	{#if orientation === "vertical" || orientation === "both"}
    <Scrollbar orientation="vertical" class={scrollbarYClasses}>
      <ScrollAreaPrimitive.Thumb
		    class={cn("relative rounded-full flex-1", scrollbarClass)}
	    />
    </Scrollbar>
  {/if}
  {#if orientation === "horizontal" || orientation === "both"}
    <Scrollbar orientation="horizontal" class={cn(scrollbarXClasses, scrollbarClass)}>
      <ScrollAreaPrimitive.Thumb
		    class={cn("relative rounded-full", scrollbarClass)}
	    />
    </Scrollbar>
  {/if}
	<ScrollAreaPrimitive.Corner />
</ScrollAreaPrimitive.Root>
