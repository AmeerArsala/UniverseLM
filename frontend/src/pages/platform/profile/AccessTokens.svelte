<script lang="ts">
  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";
  import { apiKey } from "$lib/data/stores";
  import { hasAPIKey } from "$lib/data/datafunctions";

  import * as Card from "$lib/components/ui/card/index.js";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import { Button, LoadableButton } from "$lib/components/ui/button/index.js";

  import GenerateAPIKeyDialog from "@components/GenerateAPIKey/GenerateAPIKeyDialog.svelte";

  //let generateAPIKeyOpen: boolean = false;
</script>

<Card.Root class="w-[45vw] min-h-[10vh] border-[#444460] bg-zinc-950 drop-shadow-md p-5 mt-4">
  <div class="space-y-4">
    <div>
      <!-- Header: API Keys -->
      <h1 class="font-bold text-3xl text-center">Access Tokens</h1>

      <!-- Small Description -->
      <p class="text-gray-400 text-center">Access the Power of UniverseLM</p>
    </div>

    <div class="flex flex-row justify-center">
      <!-- Button: Generate API Key -->
      <Dialog.Root>
        <Dialog.Trigger>
          <Button>Generate API Key</Button>
        </Dialog.Trigger>

        <GenerateAPIKeyDialog />
      </Dialog.Root>

    </div>
</div>
</Card.Root>
