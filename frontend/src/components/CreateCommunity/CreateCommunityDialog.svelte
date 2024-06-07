<script lang="ts">
  import CreateCommunityForm from "./CreateCommunityForm.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
</script>

<Dialog.Content>
  <CreateCommunityForm childIsCloseButton={true}>
    <Dialog.Close>
      <Button variant="outline">Cancel</Button>
    </Dialog.Close>
  </CreateCommunityForm>
</Dialog.Content>
