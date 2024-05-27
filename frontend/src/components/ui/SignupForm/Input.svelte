<script lang="ts">
	import { cn } from '$lib/utils';
	import { useMotionTemplate, useMotionValue, Motion, MotionValue } from 'svelte-motion';

	export let className: string | undefined = undefined;
	export let type: string = 'text';

	let visible = false;

	let mouseX = useMotionValue(0);
	let mouseY = useMotionValue(0);

	function handleMouseMove({ currentTarget, clientX, clientY }: any) {
		let { left, top } = currentTarget.getBoundingClientRect();

		mouseX.set(clientX - left);
		mouseY.set(clientY - top);
	}
</script>

<Motion
	let:motion
	style={{
		background: visible
			? useMotionTemplate`
  radial-gradient(
    100px circle at ${mouseX}px ${mouseY}px,
    var(--blue-500),
    transparent 80%
  )
`
			: useMotionTemplate`
  radial-gradient(
    '0px' circle at ${mouseX}px ${mouseY}px,
    var(--blue-500),
    transparent 80%
  )
`
	}}
>
	<div
		use:motion
		on:mousemove={handleMouseMove}
		on:mouseenter={() => (visible = true)}
		on:mouseleave={() => (visible = false)}
		class="group/input rounded-lg p-[2px] transition duration-300"
	>
		<input
			{type}
			class={cn(
				`dark:placeholder-text-neutral-600 duration-400 flex h-10 w-full rounded-md border-none bg-gray-50 px-3 py-2 text-sm text-black shadow-input  transition file:border-0
        file:bg-transparent file:text-sm file:font-medium placeholder:text-neutral-400
        focus-visible:outline-none focus-visible:ring-[2px]  focus-visible:ring-neutral-400 disabled:cursor-not-allowed
         disabled:opacity-50 group-hover/input:shadow-none
         dark:bg-zinc-800
         dark:text-white dark:shadow-[0px_0px_1px_1px_var(--neutral-700)] dark:focus-visible:ring-neutral-600
         `,
				className
			)}
			{...$$restProps}
		/>
	</div>
</Motion>
