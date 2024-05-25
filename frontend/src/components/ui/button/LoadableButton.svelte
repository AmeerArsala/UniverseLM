<script lang="ts">
	import { Button as ButtonPrimitive } from "bits-ui";
	import { type Events, type Props, buttonVariants } from "./index.ts";
	import { cn } from "$lib/utils/cn.ts";
  import LoaderCircle from "lucide-svelte/icons/loader-circle";

	type $$Props = Props & {
    isLoading?: boolean,
    loadingText?: string
  };

	type $$Events = Events;

	let className: $$Props["class"] = undefined;
	export let variant: $$Props["variant"] = "default";
	export let size: $$Props["size"] = "default";
	export let builders: $$Props["builders"] = [];
  export let isLoading: $$Props["isLoading"] = false;
  export let loadingText: $$Props["loadingText"] = "Please wait";
	export { className as class };
</script>

<div>
  {#if isLoading}
    <ButtonPrimitive.Root
      {builders}
      class={cn(buttonVariants({ variant, size, className }))}
      type="button"
      disabled
      {...$$restProps}
      on:click
      on:keydown
    >
      <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
      {loadingText}
    </ButtonPrimitive.Root>
  {:else}
    <ButtonPrimitive.Root
      {builders}
      class={cn(buttonVariants({ variant, size, className }))}
      type="button"
      {...$$restProps}
      on:click
      on:keydown
    >
      <slot />
    </ButtonPrimitive.Root>
  {/if}
</div>
