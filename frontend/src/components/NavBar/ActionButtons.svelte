<script lang="ts">
  import { onMount } from "svelte";

  import * as Dialog from "@components/ui/dialog/index.js";
  import SignInDialog from "@components/AuthForms/SignInDialog.svelte";
  import SignUpDialog from "@components/AuthForms/SignUpDialog.svelte";

  import { BACKEND_URL } from "$lib/data/envconfig";

  import { authentication } from "$lib/data/stores";

  import { onLogout } from "$lib/data/datafunctions";

  let authenticated: boolean = authentication.isAuthenticated();

  onMount(() => {
    authentication.getAtom().subscribe((value, oldValue) => {
      // set authenticated to the parsed boolean
      authenticated = (value === 'true');
    })
  });
</script>

<div class="space-x-2 flex flex-row">
  {#if !authenticated}
    <!--Login Button-->
    <Dialog.Root>
      <Dialog.Trigger>
        <button class="p-[3px] relative">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
          <div class="px-4 py-1.5  bg-black rounded-full relative group transition duration-200 text-white hover:bg-transparent">
            Login
          </div>
        </button>
      </Dialog.Trigger>

      <!-- Dialog content -->
      <SignInDialog />
    </Dialog.Root>

    <!--Sign Up Button-->
    <Dialog.Root>
      <Dialog.Trigger>
        <button class="group p-[3px] relative rounded-lg overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full group-hover:animate-shimmer" />
          <div class="px-4 py-1.5 relative group transition duration-200 text-white bg-transparent">
            Sign Up
          </div>
        </button>
      </Dialog.Trigger>

      <!-- Dialog content -->
      <SignUpDialog />
    </Dialog.Root>
  {:else}
    <!--Dashboard button-->
    <a href="/platform">
      <button class="group p-[3px] relative rounded-lg overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full group-hover:animate-shimmer" />
        <div class="px-4 py-1.5 relative group transition duration-200 text-white bg-transparent">
          Dashboard
        </div>
      </button>
    </a>

    <!--Log out button-->
    <a on:click={() => {
      onLogout();
      window.location.href = `${BACKEND_URL}/auth/logout`;
    }}>
      <button class="p-[3px] relative">
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
        <div class="px-4 py-1.5  bg-black rounded-full relative group transition duration-200 text-white hover:bg-transparent">
          Logout
        </div>
      </button>
    </a>
  {/if}
</div>
