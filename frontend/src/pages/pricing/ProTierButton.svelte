<script lang="ts">
  import { isYearly } from "@components/PricingPage/pricingStore";
  import { Button } from "@components/ui/button";

  export let monthlyLink: string;
  export let yearlyLink: string;
</script>

<a href={$isYearly ? yearlyLink : monthlyLink} target="_blank" class="relative inline-flex w-full items-center justify-center">
  <Button class="w-full rounded-md bg-black text-white dark:bg-white px-6 font-medium  dark:text-black transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50">
    <div class="absolute -inset-0.5 -z-10 rounded-lg bg-gradient-to-b from-[#c7d2fe] to-[#8678f9] opacity-75 blur" />
    Get started
  </Button>
</a>
