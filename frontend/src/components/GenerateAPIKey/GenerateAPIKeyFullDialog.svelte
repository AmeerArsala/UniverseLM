<script lang="ts">
  import * as Dialog from "$lib/components/ui/dialog/index.js";

  import GenerateAPIKeyDialog from "@components/GenerateAPIKey/GenerateAPIKeyDialog.svelte";
  import { generateAPIKeyOpen } from "@components/Dashboard/dashboardStores";

  const toggleGenerateAPIKeyOpen = () => { generateAPIKeyOpen.set(!$generateAPIKeyOpen); };
</script>

<Dialog.Root open={$generateAPIKeyOpen} onOpenChange={toggleGenerateAPIKeyOpen}>
  <GenerateAPIKeyDialog />
</Dialog.Root>
