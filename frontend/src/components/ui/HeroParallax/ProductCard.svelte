<script lang="ts">
	import { Motion, MotionValue } from 'svelte-motion';

	export let product: {
		title: string;
		link: string;
		thumbnail: string;
	};
	export let translate: MotionValue<number>;
</script>

<Motion
	let:motion
	style={{
		x: translate
	}}
	whileHover={{
		y: -20
	}}
>
	<div use:motion class="group/product relative h-96 w-[30rem] flex-shrink-0">
		<a href={product.link} class="block group-hover/product:shadow-2xl">
			<img
				src={product.thumbnail}
				height="600"
				width="600"
				class="absolute inset-0 h-full w-full object-cover object-left-top"
				alt={product.title}
			/>
		</a>
		<div
			class="pointer-events-none absolute inset-0 h-full w-full bg-black opacity-0 group-hover/product:opacity-80"
		></div>
		<h2 class="absolute bottom-4 left-4 text-white opacity-0 group-hover/product:opacity-100">
			{product.title}
		</h2>
	</div>
</Motion>
