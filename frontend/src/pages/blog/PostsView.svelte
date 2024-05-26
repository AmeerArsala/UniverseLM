<script lang="ts">
  import ThreeDPostCard from "./ThreeDPostCard.svelte";
  import ScrollArea from "@components/ui/scroll-area/scroll-area.svelte";
  import { type BlogPostProps } from "$lib/types/blogposts";

  import { MotionValue } from 'svelte-motion';
  //import ProductCard from "@components/ui/HeroParallax/ProductCard.svelte";

  import MovablePostCard from "./MovablePostCard.svelte";

  export let posts = [];

  export let translate: MotionValue<number>;

  function createBlogPostProps(post): BlogPostProps {
    const { title, author = "", date, description, thumbnailPath = "" } = post.frontmatter;

    return {
      title: title,
      author: author,
      date: date,
      description: description,
      thumbnailPath: thumbnailPath
    };
  }
</script>

<ScrollArea orientation="horizontal" showScrollbar={false}>
  <div class="flex flex-row justify-between space-x-3">
    {#each posts as post}
        <MovablePostCard translate={translate}>
          <a href={post.url}>
            <ThreeDPostCard postProps={createBlogPostProps(post)}/>
          </a>
        </MovablePostCard>
    {/each}
  </div>
</ScrollArea>
