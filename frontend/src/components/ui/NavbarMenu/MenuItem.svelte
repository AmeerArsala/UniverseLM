<script lang="ts">
	import { Motion } from 'svelte-motion';

	const transition = {
		type: 'spring',
		mass: 0.5,
		damping: 11.5,
		stiffness: 100,
		restDelta: 0.001,
		restSpeed: 0.001
	};

	export let active: string | null;
	export let item: string;
</script>

<div on:mouseenter={() => (active = item)} on:mouseleave={() => (active = null)} class="relative">
	<Motion let:motion transition={{ duration: 0.3 }}>
		<p use:motion class="cursor-pointer text-white hover:opacity-[0.9] dark:text-white">
			{item}
		</p>
	</Motion>
	{#if active !== null}
		<Motion
			let:motion
			initial={{ opacity: 0, scale: 0.85, y: 0 }}
			animate={{ opacity: 1, scale: 1, y: 0 }}
			{transition}
		>
			<div use:motion>
				{#if active === item}
					<div class="absolute left-1/2 -translate-x-1/2 transform pt-4">
						<Motion let:motion {transition} layoutId="active">
							<div
								use:motion
								class="overflow-hidden rounded-2xl border border-black/[0.2] bg-white shadow-xl backdrop-blur-sm dark:border-white/[0.2] dark:bg-black"
							>
								<Motion let:motion layout>
									<div use:motion class="h-full w-max p-4">
										<slot />
									</div>
								</Motion>
							</div>
						</Motion>
					</div>
				{/if}
			</div>
		</Motion>
	{/if}
</div>
