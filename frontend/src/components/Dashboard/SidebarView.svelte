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
  // TODO: create a layout for some of the common components within the '/platform' route
  import { Sidebar, type SidebarItem } from "@components/Sidebar";

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
</script>

<div class="sidebar">
  <Sidebar sidebarItems={sidebarItems}/>
</div>

<style>
  .sidebar {
    position: fixed;
    color: white;
    background: #212121;
    @apply drop-shadow-lg;
  }
</style>

