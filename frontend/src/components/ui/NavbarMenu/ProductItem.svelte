<script lang="ts">
	export let title: string;
	export let description: string;
	export let href: string;
	export let src: string;
</script>

<a {href} class="flex space-x-2">
	<img {src} width={140} height={70} alt={title} class="flex-shrink-0 rounded-md shadow-2xl" />
	<div>
		<h4 class="mb-1 text-xl font-bold text-black dark:text-white">
			{title}
		</h4>
		<p class="max-w-[10rem] text-sm text-neutral-700 dark:text-neutral-300">
			{description}
		</p>
	</div>
</a>
