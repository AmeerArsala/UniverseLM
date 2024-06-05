<script lang="ts">
  //import * as Dialog from "@components/ui/dialog/index.js";
  //import SignInDialog from "@components/AuthForms/SignInDialog.svelte";
  //import SignUpDialog from "@components/AuthForms/SignUpDialog.svelte";

  import SignInCard from "@components/AuthForms/SignInCard.svelte";
  import SignUpCard from "@components/AuthForms/SignUpCard.svelte";

  import * as Tabs from "$lib/components/ui/tabs/index.js";
</script>

<Tabs.Root value="login" class="flex flex-col justify-center items-center">
  <Tabs.List class="z-50">
    <Tabs.Trigger value="login" class="">Login</Tabs.Trigger>
    <Tabs.Trigger value="signup" class="">Sign Up</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="login" class="w-96">
    <SignInCard/>
  </Tabs.Content>
  <Tabs.Content value="signup" class="w-96">
    <SignUpCard/>
  </Tabs.Content>
</Tabs.Root>
