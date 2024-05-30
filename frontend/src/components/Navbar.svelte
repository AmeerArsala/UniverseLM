<script lang="ts">
	import { MenuItem, ProductItem, HoveredLink } from "./ui/NavbarMenu";
  import GitHubStarView from "@components/GitHubStarView.svelte";

  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import SignInDialog from "@components/AuthForms/SignInDialog.svelte";
  import SignUpDialog from "@components/AuthForms/SignUpDialog.svelte";

  import { onMount } from "svelte";
  import update, { updateAuthenticationState } from "$lib/scripts/updatestate";
  import { shouldCheckAuthentication } from "$lib/data/stores";

  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";

  import { isAuthenticated } from "$lib/data/stores";

  //let isAuthenticated: boolean = false;

	let active: string | null = null;

  onMount(async () => {
    /*if ($shouldCheckAuthentication) {
      await updateAuthenticationState();
      shouldCheckAuthentication.set(false);
    }*/
  });

  /**
   * NAVBAR ROUTES
   * Homepage (icon) [/]
   * API [/api]
   * Integrations (discord bot [/integrations/discord], slack bot [/integrations/slack], CLI [/cli])
   * About [/about]
   * Blog [/blog]
   * Pricing [/pricing]
   * GitHub Stars
   * Login [/sign-in]
   * Sign up [/sign-up]
  */
</script>

<div class="relative flex w-full items-center justify-center mt-1 mb-8">
	<div class={'inset-x-0 top-12 z-50 mx-auto flex flex-row items-center'}>
    <!--HOME-->
    <a href="/" class="absolute left-0 flex flex-row items-center">
      <img class="w-32 h-32 mr-0" src="/logo.png" alt="logo"/>
      <p class="font-inter font-bold text-2xl ml-28 absolute">UniverseLM</p>
    </a>

		<nav class="relative flex justify-center items-center space-x-12 px-8 py-6 font-bold shadow-input">
      <!--API-->
			<a href="/api" class="navbar-item">API</a>

      <!--INTEGRATIONS-->
			<MenuItem {active} item="Integrations">
				<div class="grid grid-cols-1 gap-3 p-0 text-sm">
					<ProductItem
						title="Discord Bot"
						href="/integrations/discord"
						src="/discord.png"
					/>
					<ProductItem
						title="Slack Bot"
						href="/integrations/slack"
						src="/slack.png"
					/>
					<ProductItem
						title="CLI"
						href="/cli"
						src="/cli_clipart.png"
					/>
				</div>
			</MenuItem>

      <!--ABOUT-->
      <a href="/about" class="navbar-item">About</a>

      <!--BLOG-->
      <a href="/blog" class="navbar-item">Blog</a>

      <!--PRICING-->
			<a href="/pricing" class="navbar-item">Pricing</a>

      <div class="space-x-2 flex flex-row">
        <!--GitHub-->
        <div>
          <GitHubStarView repo_link="https://github.com/AmeerArsala/UniverseLM"/>
        </div>

        {#if !$isAuthenticated}
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
          <a href="/dashboard">
            <button class="group p-[3px] relative rounded-lg overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full group-hover:animate-shimmer" />
              <div class="px-4 py-1.5 relative group transition duration-200 text-white bg-transparent">
                Dashboard
              </div>
            </button>
          </a>

          <!--Log out button-->
          <a href={`${BACKEND_URL}/auth/logout`}>
            <button class="p-[3px] relative">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
              <div class="px-4 py-1.5  bg-black rounded-full relative group transition duration-200 text-white hover:bg-transparent">
                Logout
              </div>
            </button>
          </a>
        {/if}
      </div>
		</nav>
	</div>
</div>

<style>
	.navbar-item {
    @apply hover:bg-gradient-to-r from-indigo-500 to-purple-500 hover:text-transparent bg-clip-text;
	}
</style>
