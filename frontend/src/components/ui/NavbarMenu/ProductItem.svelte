<script lang="ts">
	export let title: string;
	export let href: string;
	export let src: string;
</script>

<a {href} class="flex space-x-2">
	<img {src} width={40} height={40} alt={title} class="flex-shrink-0 rounded-md" />
	<div class="flex items-center">
		<h4 class="mb-1 text-xl font-bold text-black dark:text-white">
			{title}
		</h4>
	</div>
</a>
