<script lang="ts">
  import CardBody from "@components/ui/ThreeDCardEffect/CardBody.svelte";
  import CardContainer from "@components/ui/ThreeDCardEffect/CardContainer.svelte";
  import CardItem from "@components/ui/ThreeDCardEffect/CardItem.svelte";

  import { type BlogPostProps } from "$lib/types/blogposts";

  export let postProps: BlogPostProps = {
    title: "",
    author: "",
    date: "",
    description: "",
    thumbnailPath: ""
  };

  // Fix the value
  if (postProps.thumbnailPath === "default") {
    postProps.thumbnailPath = "/logo.png";
  }

  let includeThumbnail: boolean = postProps.thumbnailPath.length > 0;
  let includeAuthor: boolean = postProps.author.length > 0;

  let isMouseEntered: boolean = false;
</script>

<CardContainer bind:isMouseEntered className="inter-var">
	<CardBody
		className="bg-gray-50 relative group/card  dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border  "
	>
    <!--TITLE-->
		<CardItem
			{isMouseEntered}
			translateZ="50"
			className="text-xl font-bold text-neutral-600 dark:text-white"
		>
			{postProps.title}
		</CardItem>

    <!--Date [+ Author]-->
    <CardItem
			{isMouseEntered}
			translateZ="60"
			className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
		>
			{postProps.date}
      {#if includeAuthor}
        <br />
        <span class="italic">Author: {postProps.author}</span>
      {/if}
		</CardItem>

    <!--[Thumbnail]-->
		{#if includeThumbnail}
      <CardItem {isMouseEntered} translateZ="100" className="w-full mt-4">
        <img
          src={postProps.thumbnailPath}
          height="1000"
          width="1000"
          class="h-60 w-full rounded-xl object-cover group-hover/card:shadow-xl"
          alt="thumbnail"
        />
      </CardItem>
    {/if}

    <!--Description-->
    <CardItem
			{isMouseEntered}
			translateZ="60"
			className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
		>
      {postProps.description}
    </CardItem>

    <!--Read blog post option-->
		<div class="mt-20 flex items-center justify-end">
			<CardItem
				{isMouseEntered}
				translateZ={20}
				className="px-4 py-2 rounded-xl text-xs font-normal dark:text-white"
			>
				Read →
			</CardItem>
		</div>
	</CardBody>
</CardContainer>
