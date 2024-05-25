<script>
  import { LoadableButton } from "$lib/components/ui/button";

  let joinIsLoading = false;
  let previewIsLoading = false;

  function joinCommunity() {
    joinIsLoading = true;
  }

  function previewCommunity() {
    previewIsLoading = true;
  }
</script>

<div class="flex flex-row justify-center">
  <LoadableButton class="font-inter mr-3" variant="outline" isLoading={previewIsLoading} loadingText="Loading" on:click={previewCommunity}>
    Preview
  </LoadableButton>

  <LoadableButton class="font-inter" isLoading={joinIsLoading} loadingText="Joining" on:click={joinCommunity}>
    Join
  </LoadableButton>
</div>
