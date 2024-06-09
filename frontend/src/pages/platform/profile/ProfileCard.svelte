<script lang="ts">
  import { onMount } from "svelte";
  import axios from "axios";
  import { BACKEND_URL } from "$lib/data/envconfig";
  import { userAuthID } from "$lib/data/stores";
  import { type UserDetails, retrieveUserDetails } from "$lib/data/datafunctions";
  import { userDetails, userTierPlan } from "./profileStores";

  import * as Card from "$lib/components/ui/card/index.js";
  import { Badge } from "$lib/components/ui/badge/index.js";

  onMount(() => {
    // GET:
    // FULL NAME (FIRST, LAST)
    // EMAIL
    // PFP
    retrieveUserDetails().then((user_details) => {
      userDetails.set(user_details);
    });

    axios.get(`${BACKEND_URL}/user/${userAuthID.get()}/view_profile/tier_plan`, {
      withCredentials: true
    }).then((response) => {
      let tier_plan: number = response.data;

      // by index
      const TIER_PLAN = ["null", 'FREE', 'PRO', 'SCALE', 'ADMIN'];

      let tierName: string = TIER_PLAN[tier_plan];

      userTierPlan.set(tierName);
    }).catch((error) => {
      console.log("Error fetching user details: " + error);
    });
  });
</script>

<Card.Root class="w-[45vw] h-[30vh] rounded-md border-solid border-[#444460] bg-zinc-950 drop-shadow-md p-2">
  <div class="flex flex-row items-center space-x-4 p-4">
    <img class="w-64 h-64 rounded-full border-solid border-[2px] border-[#444460]" src={$userDetails.picture} alt="pfp"/>

    <div class="p-4">
      <!-- Title -->
      <h1 class="font-bold text-6xl text-center">{$userDetails.given_name} {$userDetails.family_name}</h1>

      <!-- Email -->
      <h3 class="font-bold text-2xl text-start justify-self-start">{$userDetails.email}</h3>

      <!-- Plan Badge -->
      <Badge class="absolute left-2 top-2">{$userTierPlan}</Badge>
    </div>
  </div>
</Card.Root>
