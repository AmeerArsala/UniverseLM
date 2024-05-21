<script lang="ts">
	import { MenuItem, ProductItem, HoveredLink } from "./ui/NavbarMenu";

	let active: string | null = null;

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

<div class="relative flex w-full items-center justify-center">
	<div class={'inset-x-0 top-12 z-50 mx-auto'}>
		<nav class="relative flex justify-center space-x-12 bg-black px-8 py-6 shadow-input">
      <!--HOME-->

      <!--API-->
			<a class="text-white" href="/api">API</a>

      <!--INTEGRATIONS-->
			<MenuItem {active} item="Integrations">
				<div class="grid grid-cols-1 gap-10 p-4 text-sm">
					<ProductItem
						title="Discord Bot"
						href="#"
						src="/discord.png"
					/>
					<ProductItem
						title="Slack Bot"
						href="#"
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
      <a class="text-white" href="/about">About</a>

      <!--BLOG-->
      <a class="text-white" href="/blog">Blog</a>

      <!--PRICING-->
			<a class="text-white" href="/pricing">Pricing</a>

      <!--GitHub-->

      <!--Login Button-->

      <!--Sign Up Button-->
		</nav>
	</div>
</div>
