<script lang="ts">
  import axios from "axios";
  import { authState/*, userAuthID, coreRegistration*/ } from "$lib/data/stores";

  import { idNotFound, onLogout } from "$lib/data/datafunctions";

  export let href: string;

  function handleAuth() {
    // First things first: delete the current userAuthID if it exists
    // Make sure the state is reset
    onLogout();

    let realHref: string = href + "&redirect=false";

    axios.get(realHref, { withCredentials: true })
    //.then((response) => response.json())  // wow, this worked better than response.text(). fuck you JS!!!
    .then((response) => {
      const text: string = response.data;

      console.log("DONE!")
      console.log(text);

      const url: string = text;

      // Add the data to a store
      // get state first
      const key: string = "state=";

      let state: string = url.substring(url.indexOf(key)+key.length);
      const endIndex: number = state.indexOf("&");

      if (endIndex !== -1) {
        state = state.substring(0, endIndex);
      }

      // SET IT SO IT CAN BE USED LATER TO AUTHENTICATE
      authState.set(state);

      // Faciliate the redirect
      // Do not store this in browser history, hence why we use replace and not just do `window.location.href = url;`
      window.location.replace(url);
    }).catch((error) => {
      console.log(error);
      console.log("Error getting auth");
    });
  }
</script>

<div on:click={handleAuth}>
  <slot />
</div>
