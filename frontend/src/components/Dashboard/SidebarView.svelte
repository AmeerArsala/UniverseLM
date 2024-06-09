<script lang="ts">
  /**
   * Home (Dashboard overview, my societies, my agents (like a pokemon storage PC of them), daily stats, most popular agents, etc.)
   * Society/Community Explorer (Explore public ones)
   * Society/Community Creator
   * Docs
   * Billing
   * Profile (for API Key gen, stats, etc.)
  */

  // ALSO make sure to include a search bar w/ keyboard shortcuts to shortcut actions
  import { Sidebar, type SidebarItem } from "@components/Sidebar";
  import { fade } from 'svelte/transition';
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import CreateCommunityDialog from "@components/CreateCommunity/CreateCommunityDialog.svelte";
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";

  import {
    IconHome,           // Dashboard home
    IconTopologyRing,   // Explore Communities
    IconSquarePlus,     // Create community
    IconFileLambda,     // Docs
    IconWallet,         // Billing
    IconUser,           // Profile
  } from '@tabler/icons-svelte';

  const sidebarItems: SidebarItem[] = [
    {
      text: "Home",
      iconComponent: IconHome,
      href: "/platform",
      target: "_self",
    },
    {
      text: "Explore Communities",
      iconComponent: IconTopologyRing,
      href: "/platform/explore",
      target: "_self"
    },
    // this one is not rendered; the object is just a placeholder @ index = 2
    {
      text: "Create Community",
      iconComponent: IconSquarePlus,
      href: "/platform/create-society",
      target: "_self"
    },
    {
      text: "Docs",
      iconComponent: IconFileLambda,
      href: "/platform/docs",
      target: "_blank"
    },
    {
      text: "Billing",
      iconComponent: IconWallet,
      href: "/platform/billing",
      target: "_self"
    },
    {
      text: "Profile",
      iconComponent: IconUser,
      href: "/platform/profile",
      target: "_self"
    }
  ];

  let expanded: boolean = false;

  // same as Sidebar.svelte
  const fadeIn = {
		delay: 100,
		duration: 200
	};

	const fadeOut = {
		delay: 0,
		duration: 100
	};

  let isCtrlOrCmdDown: boolean = false;
  let isPeriodDown: boolean = false;

  let createCommunityOpen: boolean = false;

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
      case ".":
        isPeriodDown = true;

        if (isCtrlOrCmdDown) {
          event.preventDefault();
        }
        break;
    }

    if (isCtrlOrCmdDown && isPeriodDown) {
      createCommunityOpen = true;
    }
  }

  function onKeyUp(event) {
    switch (event.key) {
      case "Control":
      case "Meta":
        isCtrlOrCmdDown = false;
        event.preventDefault();
        break;
      case ".":
        isPeriodDown = false;
        event.preventDefault();
        break;
    }
  }
</script>

<svelte:window
  on:keydown={handleKeyDown}
  on:keyup={onKeyUp}
/>

<div class="sidebar">
  <Sidebar sidebarItems={sidebarItems} customIndex={2} bind:isExpanded={expanded}>
    <!-- The custom item (the 'create a new community button') -->
    <Tooltip.Root openDelay={750}>
      <Tooltip.Trigger asChild={true}>
        <Dialog.Root open={createCommunityOpen} onOpenChange={() => { createCommunityOpen = !createCommunityOpen; }}>
          <Dialog.Trigger>
            <div class="relative flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground" on:click={() => { createCommunityOpen = !createCommunityOpen; }}>
              <IconSquarePlus class="h-6 w-6 text-neutral-800 dark:text-neutral-300"/>
              {#if expanded}
                <div class="sidebar-item-text">
                  <span class="absolute left-7" in:fade="{fadeIn}" out:fade="{fadeOut}">Create Community</span>
                </div>
              {/if}
            </div>
          </Dialog.Trigger>

          <CreateCommunityDialog />
        </Dialog.Root>
      </Tooltip.Trigger>

      <Tooltip.Content>
        <p>Create new Community (⌘ + .)</p>
      </Tooltip.Content>
    </Tooltip.Root>

  </Sidebar>
</div>

<style>
  .sidebar {
    position: fixed;
    color: white;
    background: #212121;
    @apply drop-shadow-lg;
  }
</style>

<!--
<Dialog.Root open={createCommunityOpen} onOpenChange={() => { createCommunityOpen = !createCommunityOpen; }}>
      <Dialog.Trigger>
        <div class="relative flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground" on:click={() => { createCommunityOpen = !createCommunityOpen; }}>
          <IconSquarePlus class="h-6 w-6 text-neutral-800 dark:text-neutral-300"/>
          {#if expanded}
            <span class="absolute left-10" in:fade="{fadeIn}" out:fade="{fadeOut}">Create Community</span>
          {/if}
        </div>
      </Dialog.Trigger>

      <CreateCommunityDialog />
    </Dialog.Root>


<Tooltip.Root>
          <Tooltip.Trigger asChild let:builder>

            <div class="flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground">
              <IconSquarePlus class="h-6 w-6 text-neutral-800 dark:text-neutral-300"/>
              {#if expanded}
                <span class="absolute left-10" in:fade="{fadeIn}" out:fade="{fadeOut}">Create Community</span>
              {/if}
            </div>
          </Tooltip.Trigger>
          <Tooltip.Content>
            <p>Create new Community (⌘ + .)</p>
          </Tooltip.Content>
        </Tooltip.Root>

<Tooltip.Root openDelay={750}>
      <Tooltip.Trigger asChild={true}>
        <Dialog.Root open={createCommunityOpen} onOpenChange={() => { createCommunityOpen = !createCommunityOpen; }}>
          <Dialog.Trigger>
            <div class="relative flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground" on:click={() => { createCommunityOpen = !createCommunityOpen; }}>
              <IconSquarePlus class="h-6 w-6 text-neutral-800 dark:text-neutral-300"/>
              {#if expanded}
                <span class="absolute left-10" in:fade="{fadeIn}" out:fade="{fadeOut}">Create Community</span>
              {/if}
            </div>
          </Dialog.Trigger>

          <CreateCommunityDialog />
        </Dialog.Root>
      </Tooltip.Trigger>

      <Tooltip.Content>
        <p>Create new Community (⌘ + .)</p>
      </Tooltip.Content>
    </Tooltip.Root>

<Dialog.Root open={createCommunityOpen} onOpenChange={() => { createCommunityOpen = !createCommunityOpen; }}>
      <Dialog.Trigger>
        <Tooltip.Root openDelay={750}>
          <Tooltip.Trigger asChild={true}>
            <div class="relative flex flex-row space-x-2 hover:bg-accent hover:text-accent-foreground" on:click={() => { createCommunityOpen = !createCommunityOpen; }}>
              <IconSquarePlus class="h-6 w-6 text-neutral-800 dark:text-neutral-300"/>
              {#if expanded}
                <span class="absolute left-10" in:fade="{fadeIn}" out:fade="{fadeOut}">Create Community</span>
              {/if}
            </div>
          </Tooltip.Trigger>

          <Tooltip.Content>
            <p>Create new Community (⌘ + .)</p>
          </Tooltip.Content>
        </Tooltip.Root>
      </Dialog.Trigger>

      <CreateCommunityDialog />
    </Dialog.Root>
-->
