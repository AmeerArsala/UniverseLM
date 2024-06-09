<script lang="ts">
  import { onMount } from "svelte";
  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";
  import { userAuthID } from "$lib/data/stores";

  import * as Card from "$lib/components/ui/card/index.js";

  import { marked } from "marked";
  import { userREADMEmd } from "./profileStores";

  let content;
  let contentLoaded: boolean = false;

  onMount(() => {
    // Fetch the markdown
    axios.get(`${BACKEND_URL}/user/${userAuthID.get()}/view_profile/readme`, {
      withCredentials: true
    }).then((response) => {
      userREADMEmd.set(response.data);

      content = marked.parse($userREADMEmd);
      contentLoaded = true;
    }).catch((error) => {
      console.log("Error fetching user README: " + error);
    });

  });

</script>

<Card.Root class="w-[45vw] min-h-[50vh] border-[#444460] bg-zinc-950 drop-shadow-md p-6">
  {#if contentLoaded}
    <article class="prose prose-neutral lg:prose-lg dark:prose-invert">
      <!-- Markdown Content  -->
      {@html content}
    </article>
  {:else}
    <p>Loading README...</p>
  {/if}
</Card.Root>
