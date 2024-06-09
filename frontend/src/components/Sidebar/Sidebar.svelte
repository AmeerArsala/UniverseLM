<script lang="ts">
  import { fade } from 'svelte/transition';
  import { Button } from "$lib/components/ui/button/index.js";
  //import * from '@tabler/icons-svelte';
  import {
    IconLayoutSidebar
  } from '@tabler/icons-svelte';

  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import { type SidebarItem } from "./index";

	const fadeIn = {
		delay: 100,
		duration: 200
	};

	const fadeOut = {
		delay: 0,
		duration: 100
	};

  export let isExpanded = false;

  $: tooltipText = isExpanded ? "Collapse sidebar (⌘ + B)" : "Expand sidebar (⌘ + B)";

  let isCtrlOrCmdDown: boolean = false;
  let isBKeyDown: boolean = false;

  function handleKeyDown(event) {
    // Only want to handle first press
    if (event.repeat) {
      return;
    }

    switch (event.key) {
      case "Control":
      case "Meta":
        isCtrlOrCmdDown = true;

        event.preventDefault();
        break;
      case "b":
        isBKeyDown = true;
        event.preventDefault();
        break;
    }

    if (isCtrlOrCmdDown && isBKeyDown) {
      isExpanded = !isExpanded;
    }
  }

  function onKeyUp(event) {
    switch (event.key) {
      case "Control":
      case "Meta":
        isCtrlOrCmdDown = false;
        event.preventDefault();
        break;
      case "b":
        isBKeyDown = false;
        event.preventDefault();
        break;
    }
  }

  export let itemStyle: string = "flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground";
  export let iconStyle: string = "h-6 w-6 text-neutral-800 dark:text-neutral-300";
  export let spanStyle: string = "absolute left-10";

  export let sidebarWidth: string = "60px";
  const sidebarStyle: string = `p-3 h-screen space-y-6 w-[${sidebarWidth}] bg-black drop-shadow-md`;

  export let sidebarItems: SidebarItem[] = [];

  export let customIndex: number = -1;
</script>

<svelte:window
  on:keydown={handleKeyDown}
  on:keyup={onKeyUp}
/>

<nav class:expanded={isExpanded} class={sidebarStyle}>
  <Tooltip.Root openDelay={250}>
    <Tooltip.Trigger asChild let:builder>
      <!-- Icon for expand collapse -->
      <Button builders={[builder]} variant="ghost" on:click={() => isExpanded = !isExpanded} class="p-0 flex justify-start">
        <IconLayoutSidebar class="h-6 w-6 text-neutral-800 dark:text-neutral-300" />
      </Button>
    </Tooltip.Trigger>
    <Tooltip.Content>
      <p>{tooltipText}</p>
    </Tooltip.Content>
  </Tooltip.Root>

	<div class="flex flex-col justify-center space-y-6 text-nowrap">
		{#each sidebarItems as item, i}
      {#if i === customIndex}
        <slot />
      {:else}
        <a href={item.href} target={item.target} class={itemStyle}><svelte:component this={item.iconComponent} class={iconStyle}/>{#if isExpanded}<span class={spanStyle} in:fade="{fadeIn}" out:fade="{fadeOut}">{item.text}</span>{/if}</a>
      {/if}
    {/each}
	</div>
</nav>

<style>
	nav {
		grid-area: nav;
		transition: ease-out 200ms;
		overflow: hidden;
	}

	.expanded {
		transition: ease-out 200ms;
		width: 250px;
	}
</style>
