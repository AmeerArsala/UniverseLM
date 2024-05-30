<script>
  import { Button } from "@components/ui/button"
  import * as Dialog from "@components/ui/dialog";
  import SignUpDialog from '@components/AuthForms/SignUpDialog.svelte'
</script>

<div class="w-full items-center inline-flex">
  <Dialog.Root>
    <Dialog.Trigger>
      <Button class="w-[250%] relative justify-center inline-flex items-center rounded-md bg-black text-white dark:bg-white px-6 font-medium dark:text-black transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50">
        <div class="absolute -inset-0.5 -z-10 rounded-lg bg-gradient-to-b from-[#c7d2fe] to-[#8678f9] opacity-75 blur" />
        Sign up
      </Button>
    </Dialog.Trigger>

    <!--TODO: Make this only happen if not signed in-->
    <SignUpDialog/>
  </Dialog.Root>
</div>
