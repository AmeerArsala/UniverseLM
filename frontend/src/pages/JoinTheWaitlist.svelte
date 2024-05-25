<script lang="ts">
	import { BackgroundBeams } from '$lib/components/ui/BackgroundBeams';
</script>

<div
	class="relative flex h-[40rem] w-full flex-col items-center justify-center rounded-md px-32 antialiased"
>
	<div class="mx-auto max-w-2xl p-4">
		<h2
			class="relative z-10 bg-gradient-to-b from-neutral-200 to-neutral-600 bg-clip-text text-center font-sans text-lg font-bold text-transparent md:text-7xl"
		>
			Join the waitlist
		</h2>
		<p></p>
		<p class="relative z-10 mx-auto my-2 max-w-lg text-center text-sm text-neutral-500">
			Welcome to UniverseLM, the best place on to run AI simulations.
		</p>
		<input
			type="text"
			placeholder="hello@example.com"
			class="relative z-10 mt-4 w-full rounded-lg border border-neutral-800 bg-neutral-950 p-2 placeholder:text-neutral-700 focus:ring-2 focus:ring-teal-500"
		/>
	</div>
	<BackgroundBeams />
</div>
