<script lang="ts">
  import axios from "axios";
  import { authState } from "$lib/data/stores";

  export let href: string;

  function handleAuth() {
    let realHref: string = href + "&redirect=false";

    axios.get(realHref).then((response) => {
      console.log("DONE!")
      console.log(response.data);

      const url: string = response.data;

      // Add the data to a store
      // get state first
      const key: string = "state=";

      let state: string = url.substring(url.indexOf(key)+key.length);
      const endIndex: number = state.indexOf("&");

      if (endIndex !== -1) {
        state = state.substring(0, endIndex);
      }

      // SET IT
      authState.set(state);

      // Faciliate the redirect
      // Do not store this in browser history, hence why we use replace and not just do `window.location.href = url;`
      window.location.replace(url);
    }).catch((error) => {
      console.log("Error getting auth");
    })
  }
</script>

<div on:click={handleAuth}>
  <slot />
</div>
