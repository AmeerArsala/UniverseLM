<script lang="ts">
  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";
  import { apiKey } from "$lib/data/stores";
  import { hasAPIKey } from "$lib/data/datafunctions";

  import { Button, LoadableButton } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Textarea } from "$lib/components/ui/textarea/index.js";

  import TagsInput from "@components/TagsInput.svelte";

  export let childIsCloseButton: boolean = false;

  $: footerStyle = childIsCloseButton ? "flex justify-between" : "flex justify-end"

  /**
    - Name
    - Public or Private (only allowed on paid plans)
    - AI Generated Base (optional; reveal the following if checked)
      - Community Description (optional)
      - Number of Agents/Chunks (optional)

    Extra
    - Invite Owners (emails)
    - Invite to whitelist (if private, and invited owners will automatically be invited)
  */

  // Community Name
  let name: string = "";

  let isPrivate: boolean = false; // if this is selected, once confirmed, make sure to reject if the user is on free tier

  let isAIGeneratedBase: boolean = false;
  // only show thes if isAIGeneratedBase is checked
  let communityDescription: string = "";
  let numChunksStr: string = "";

  // Extra
  let invitedOwnersEmails: string[] = [];
  let invitedWhitelistEmails: string[] = [];  // only show if private is checked

  // Submissions
  let submissionIsLoading: boolean = false;

  // rejections
  let nameRejected: boolean = false;
  let privateRejected: boolean = false;

  let nameRejectionMessage: string = "Name invalid";
  let privacyRejectionMessage: string = "Private communities are not allowed in the Free Tier.";

  let alertGenerateAPIKey: boolean = false;

  interface SubmissionResponse {
    success: boolean,
    name_allowed: boolean,
    privacy_allowed: boolean,
    name_status_message: string,
    privacy_status_message: string,
    community_id: number
  }

  function parseNumChunks(): number {
    let parsedNumChunks: number = parseInt(numChunksStr);

    if (isNaN(parsedNumChunks)) {
      parsedNumChunks = -1; // the default that signifies not caring about it
    }

    return parsedNumChunks;
  }

  function onSubmit(...args) {
    if (!hasAPIKey()) {
      alertGenerateAPIKey = true;
      return;
    }

    submissionIsLoading = true;

    axios.post(`${BACKEND_URL}/apotheosis/community`, {
      params: {
        name: name,
        private: isPrivate,
        ai_generate_base: isAIGeneratedBase,
        community_desc: communityDescription,
        num_chunks: parseNumChunks(),
        invited_owners_emails: invitedOwnersEmails,
        invited_whitelisted_emails: invitedWhitelistEmails
      }
    }, {
      headers: {
        'UniverseLM-API-Key': $apiKey
      }
    }).then((response) => {
      let result: SubmissionResponse = response.data;

      submissionIsLoading = false;

      if (result.success) {
        //TODO: open community with result.community_id
      } else {
        nameRejected = (result.name_allowed === false);
        privateRejected = (result.privacy_allowed === false);

        nameRejectionMessage = result.name_status_message;
        privacyRejectionMessage = result.privacy_status_message;
      }
    }).catch((error) => {
      console.log("Error with submitting form to create community: " + error);
    });

  }
</script>

<Card.Root class="border-none">
  <Card.Header>
    <Card.Title>New Community</Card.Title>
    <Card.Description>Create a community</Card.Description>
    {#if alertGenerateAPIKey}
      <p class="font-bold text-red-600">You Must Generate an API Key first in order to use UniverseLM. Do so by heading to your <a href="/platform/profile" class="underline underline-offset-1 text-blue-500">profile</a></p>
    {/if}
  </Card.Header>
  <Card.Content>
    <form>
      <div class="grid w-full items-center gap-4">
        <!-- Name -->
        <div class="flex flex-col space-y-1.5">
          <Label for="name">Community Name</Label>
          <Input id="name" placeholder="Name of your society" bind:value={name} />

          {#if nameRejected}
            <p class="text-sm text-red-700">{nameRejectionMessage}</p>
          {/if}
        </div>
        <div class="flex flex-col space-y-3.5">
          <!-- Public or Private Checkbox -->
          <div class="items-top flex space-x-2">
            <Checkbox id="is_private" bind:checked={isPrivate} />
            <div class="grid gap-1.5 leading-none">
              <Label
                for="is_private"
                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Private
              </Label>

              {#if privateRejected}
                <p class="text-sm text-red-700">{privacyRejectionMessage}</p>
              {/if}
            </div>
          </div>

          <!-- AI Generated Base Checkbox -->
          <div class="flex items-center space-x-2">
            <Checkbox id="ai-generated-base" bind:checked={isAIGeneratedBase} aria-labelledby="ai-generated-base-label" />
            <Label
              id="ai-generated-base-label"
              for="ai-generated-base"
              class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Generate a Base with AI
            </Label>
          </div>

          {#if isAIGeneratedBase}
            <!-- Community Description (optional) -->
            <div class="flex flex-col space-y-1.5">
              <Label for="community-desc">Community Description (optional)</Label>
              <Textarea id="community-desc" placeholder="Community Description" bind:value={communityDescription}/>
            </div>

            <!-- Number of Agents/Chunks (optional) -->
            <div class="flex flex-col space-y-1.5">
              <Label for="num-chunks">Number of Agents/Chunks (optional)</Label>
              <Input id="num-chunks" placeholder="0" bind:value={numChunksStr} />
            </div>
          {/if}

          <br/>

          <!-- Invite Owners Emails (optional) -->
          <div class="flex flex-col space-y-1.5">
            <Label for="owners-emails-input">Add Owners' Emails (optional)</Label>
            <TagsInput
              id="owners-emails-input"
              placeholderText="yourfriend@example.com and press 'Enter'"
              bind:tag_names={invitedOwnersEmails}
            />
          </div>


          <!-- Invite to whitelist emails (only show if isPrivate) -->
          {#if isPrivate}
            <!-- Invite to Whitelist Emails (optional) -->
            <div class="flex flex-col space-y-1.5">
              <Label for="whitelisted-emails-input">Add Whitelisted Emails (optional)</Label>
              <TagsInput
                id="whitelisted-emails-input"
                placeholderText="yourfriend@example.com and press 'Enter'"
                bind:tag_names={invitedWhitelistEmails}
              />
            </div>
          {/if}
        </div>
      </div>
    </form>
  </Card.Content>
  <Card.Footer class={footerStyle}>
    <!-- <Button variant="outline">Cancel</Button> -->
    {#if childIsCloseButton}
      <slot />
    {/if}

    <LoadableButton on:click={onSubmit} isLoading={submissionIsLoading}>Create</LoadableButton>
  </Card.Footer>
</Card.Root>
