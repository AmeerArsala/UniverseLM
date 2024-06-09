<script lang="ts">
  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";
  import { apiKey, userAuthID } from "$lib/data/stores";

  import * as Card from "$lib/components/ui/card/index.js";
  import { Button, LoadableButton } from "$lib/components/ui/button/index.js";
  import * as Select from "$lib/components/ui/select";
  import { Label } from "$lib/components/ui/label/index.js";

  import { Calendar } from "$lib/components/ui/calendar/index.js";
  //import CalendarIcon from "lucide-svelte/icons/calendar";
  import {
    getLocalTimeZone,
    today
  } from "@internationalized/date";

  import { copyTextToClipboard, saveTextFile } from "$lib/scripts/utilities";

  import { IconCopy, IconCheck, IconDownload } from "@tabler/icons-svelte";

  /**
   * OPTIONS:
   * 1 week
   * 1 month
   * 3 months
   * 6 months
   * 1 year
   * Never
   * Custom
   */

  // Custom exists as well but will be added manually
  const ttlOptions = [
    { label: "1 week", value: "week"},
    { label: "1 month", value: "month" },
    { label: "3 months", value: "quarter" },
    { label: "6 months", value: "half-year" },
    { label: "1 year", value: "year" },
    { label: "Never", value: "never" }
  ];

  let expirationTTLFormValue = ttlOptions[1]; // month
  $: expirationTTL = expirationTTLFormValue.value;

  const TODAY = today(getLocalTimeZone());
  const MIN_EXPIRATION_DATE = TODAY.add({days: 1});  // TOMORROW

  let calendarTTLDate = MIN_EXPIRATION_DATE;

  // Durations
  const WEEK = 7, MONTH = 30, YEAR = 365,
        QUARTER = (MONTH * 3), HALF_YEAR = (MONTH * 6),
        NEVER = -1; // -1 is the default on the backend for no expiration date

  function ttlToDays(): number {
    switch (expirationTTL) {
      case "week":
        return WEEK;
      case "month":
        return MONTH;
      case "quarter":
        return QUARTER;
      case "half-year":
        return HALF_YEAR;
      case "year":
        return YEAR;
      case "never":
        return NEVER;
      case "custom":
        // Convert to JS Date objects
        const startDate = TODAY.toDate();
        const endDate = calendarTTLDate.toDate();

        // Calculate the difference in days
        const diffInDays: number = Math.ceil(Math.abs((endDate - startDate) / (1000 * 60 * 60 * 24)));
        return diffInDays;
      default:
        console.log("WTF: date error");
        return NEVER;
    }
  }

  let generationLoading: boolean = false;
  let generationComplete: boolean = false;

  function generateAPIKey() {
    generationLoading = true;
    generationComplete = false;

    const ttl: number = ttlToDays();
    console.log("TTL Days: " + ttl);

    let params = {};

    if (ttl !== NEVER) {
      // Add expiration ttl
      const SECONDS_PER_DAY = 24 * 60 * 60;
      const ttlSeconds: number = ttl * SECONDS_PER_DAY;

      params = {
        ...params,
        expiration_ttl_seconds: ttlSeconds
      };
    }

    // Make the POST request
    axios.post(`${BACKEND_URL}/user/${userAuthID.get()}/create_apikey`, {
      params: params
    },
    { withCredentials: true }).then((response) => {
      const apikey: string = response.data;

      apiKey.set(apikey);

      generationLoading = false;
      generationComplete = true;
    })
  }

  let apiKeyCopiedByUser: boolean = false;
</script>

<Card.Root class="border-none">
  {#if !generationComplete || generationLoading}
    <Card.Header>
      <Card.Title>Generate an API Key</Card.Title>
      <Card.Description>Generate an API Key to use UniverseLM</Card.Description>
    </Card.Header>

    <Card.Content>
      <!-- Expiration Time (options: 1 week, 1 month, 3 months, 6 months, 1 year, Never, Custom [view: Calendar -> NoUserEdit]) -->
      <div class="expiration-select space-y-2">
        <Label class="font-bold">Expiration Date</Label>
        <Select.Root
          selected={expirationTTLFormValue}
          onSelectedChange={(v) => {
            v && (expirationTTL = v.value);
          }}
        >
          <Select.Trigger>
            <Select.Value placeholder="Expiration Time"/>
          </Select.Trigger>

          <Select.Content>
            {#each ttlOptions as option}
              <Select.Item value={option.value} label={option.label}>{option.label}</Select.Item>
            {/each}

            <!-- Custom Option: Calendar -->
            <Select.Item value="custom" label="Custom">Custom</Select.Item>
          </Select.Content>
        </Select.Root>

        {#if expirationTTL === "custom"}
          <Calendar bind:value={calendarTTLDate} minValue={MIN_EXPIRATION_DATE} class="rounded-md border"/>
        {/if}
      </div>

      <br />

      <!-- Warning Label -->
      <Label class="font-bold">WARNING: Any previous API Key you have generated will be <span class="underline">overwritten</span> by this key</Label>

      <!-- Generate Button (LoadableButton) -->
      <LoadableButton on:click={generateAPIKey} isLoading={generationLoading} class="mt-4">Generate</LoadableButton>
    </Card.Content>
  {:else}
    <!-- After an API Key has been generated -->
    <Card.Header>
      <Card.Title>API Key</Card.Title>
      <Card.Description>🎉 Congratulations! You have generated an API Key!</Card.Description>
    </Card.Header>

    <Card.Content>
      <Label class="font-bold">API Key</Label>

      <!-- The actual API Key -->
      <div class="p-4">
        <code class="rounded-sm">
          {$apiKey}
        </code>

        <!-- Copy button -->
        <div class="flex flex-row absolute right-3 top-1 bottom-1">
          {#if !apiKeyCopiedByUser}
            <IconCopy on:click={() => {
              copyTextToClipboard($apiKey);
              apiKeyCopiedByUser = true;
            }}
            />
          {:else}
            <IconCheck class="fill-green-600"/>
          {/if}

          <IconDownload on:click={async () => { saveTextFile($apiKey); }}/>
        </div>
      </div>


      <!-- Blah blah blah do not show this to anyone -->
      <Label class="text-red-600">Make sure to save this somewhere <span class="underline">safe</span> because we will <span class="font-bold underline">not</span> show this key again</Label>
    </Card.Content>
  {/if}
</Card.Root>

<style>
  .expiration-select {

  }
</style>
