<script lang="ts">
	export let products: {
		title: string;
		link: string;
		thumbnail: string;
	}[];

	import { Motion, useTransform, useSpring, useViewportScroll } from 'svelte-motion';
	import ProductCard from './ProductCard.svelte';

	const firstRow = products.slice(0, 5);
	const secondRow = products.slice(5, 10);
	const thirdRow = products.slice(10, 15);
	let ref: HTMLDivElement | null = null;

	const { scrollYProgress } = useViewportScroll();

	const springConfig = { stiffness: 300, damping: 30, bounce: 100 };

	const translateX = useSpring(useTransform(scrollYProgress, [0, 1], [0, 1000]), springConfig);
	const translateXReverse = useSpring(
		useTransform(scrollYProgress, [0, 1], [0, -1000]),
		springConfig
	);
	const rotateX = useSpring(useTransform(scrollYProgress, [0, 0.2], [15, 0]), springConfig);
	const opacity = useSpring(useTransform(scrollYProgress, [0, 0.2], [0.2, 1]), springConfig);
	const rotateZ = useSpring(useTransform(scrollYProgress, [0, 0.2], [20, 0]), springConfig);
	const translateY = useSpring(useTransform(scrollYProgress, [0, 0.2], [-700, 500]), springConfig);
</script>

<div
	bind:this={ref}
	class="relative flex h-[300vh] flex-col self-auto overflow-hidden py-4 antialiased [perspective:1000px] [transform-style:preserve-3d]"
>
	<div class="relative left-0 top-0 mx-auto w-full max-w-7xl px-4 py-8 md:py-4">
		<h2 class="text-2xl font-bold dark:text-white md:text-7xl">
			See What's New with <br /> UniverseLM
		</h2>
		<p class="mt-8 max-w-2xl text-base dark:text-neutral-200 md:text-xl">
			UniverseLM is the single source of truth in this world.
		</p>
	</div>
	<Motion
		let:motion
		style={{
			rotateX,
			rotateZ,
			translateY,
			opacity
		}}
	>
		<div use:motion>
			<Motion let:motion>
				<div use:motion class="mb-20 flex flex-row-reverse space-x-20 space-x-reverse">
					{#each firstRow as product (product.title)}
						<ProductCard {product} translate={translateX} />
					{/each}
				</div>
			</Motion>
			<Motion let:motion>
				<div use:motion class="mb-20 flex flex-row space-x-20">
					{#each secondRow as product (product.title)}
						<ProductCard {product} translate={translateXReverse} />
					{/each}
				</div>
			</Motion>
			<Motion let:motion>
				<div use:motion class="flex flex-row-reverse space-x-20 space-x-reverse">
					{#each thirdRow as product (product.title)}
						<ProductCard {product} translate={translateX} />
					{/each}
				</div>
			</Motion>
		</div>
	</Motion>
</div>
