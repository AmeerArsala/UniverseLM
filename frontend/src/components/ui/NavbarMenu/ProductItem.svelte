<script lang="ts">
	export let title: string;
	export let href: string;
	export let src: string;
</script>

<a {href} class="flex space-x-2 group">
	<img {src} width={40} height={40} alt={title} class="flex-shrink-0 rounded-md" />
	<div class="flex items-center">
		<h4 class="mb-1 text-xl font-bold group-hover:bg-gradient-to-r from-indigo-500 to-purple-500 group-hover:text-transparent bg-clip-text">
			{title}
		</h4>
	</div>
</a>
