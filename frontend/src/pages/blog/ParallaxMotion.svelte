<script lang="ts">
  import { Motion, useTransform, useSpring, useViewportScroll } from 'svelte-motion';
  import PostsView from './PostsView.svelte';

  export let newsPosts = [];     // News
  export let researchPosts = []; // Research
  export let regularPosts = [];  // Posts

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
  <slot />

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
      <h3 class="section-title">News</h3>
      <Motion let:motion>
				<div use:motion class="mb-20 flex flex-row-reverse space-x-20 space-x-reverse">
					<div class="section">
            <PostsView posts={newsPosts} translate={translateX}/>
          </div>
				</div>
			</Motion>

      <h3 class="section-title">Research</h3>
			<Motion let:motion>
				<div use:motion class="mb-20 flex flex-row space-x-20">
					<div class="section">
            <PostsView posts={researchPosts} translate={translateXReverse}/>
          </div>
				</div>
			</Motion>

      <h3 class="section-title">Posts</h3>
      <Motion let:motion>
				<div use:motion class="flex flex-row-reverse space-x-20 space-x-reverse">
					<div class="section">
            <PostsView posts={regularPosts} translate={translateX}/>
          </div>
				</div>
			</Motion>
    </div>
  </Motion>
</div>

<style>
  .section-title {
    @apply font-bold text-5xl ml-32 font-neue absolute mt-3 text-start;
  }

  .section {
    @apply p-0;
  }
</style>
