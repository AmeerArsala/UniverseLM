<script lang="ts">
	import { cn } from '$lib/utils';
	import { IconBrandGithub, IconBrandGoogle, IconBrandDiscord, IconBrandSlack, IconBrandOnlyfans, IconBrandFortnite } from '@tabler/icons-svelte';
	import { Input, Label, EmailInput } from '@components/ui/SignupForm';
  import * as Dialog from "$lib/components/ui/dialog/index.js";

  import { BACKEND_URL } from "$lib/data/envconfig";

  const email_password_href_prefix: string = `${BACKEND_URL}/auth/register?method=email_password`;

  const github_href: string = `${BACKEND_URL}/auth/register?method=github`;
  const google_href: string = `${BACKEND_URL}/auth/register?method=google`;
  const slack_href: string = `${BACKEND_URL}/auth/register?method=slack`;

  // Bind this value to what the user typed
  let email = "";

  $: email_password_href = email_password_href_prefix + `&email=${encodeURIComponent(email)}`;

	const handleSubmit = (e: SubmitEvent) => {
		e.preventDefault();
		console.log('Form submitted');
	};
</script>

<Dialog.Content
	class="mx-auto w-full max-w-md rounded-none border border-gray-300 bg-white p-4 shadow dark:border-gray-800 dark:bg-black md:rounded-2xl md:p-8 form-box-shadow"
>
  <Dialog.Header>
    <h2 class="text-xl font-bold text-neutral-800 dark:text-neutral-200">Welcome to UniverseLM</h2>
  </Dialog.Header>

  <Dialog.Description>
    <div class="mt-2 max-w-sm text-sm text-neutral-600 dark:text-neutral-300">
      Sign Up for UniverseLM
    </div>
  </Dialog.Description>

	<form class="my-8" on:submit={handleSubmit}>
		<div class={'mb-4 flex w-full flex-col space-y-2'}>
			<Label htmlFor="email">Email Address</Label>
			<EmailInput id="email" placeholder="youremail@example.com" bind:value={email} />
		</div>

    <div>
      <a href={email_password_href}>
        <button
          class="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-black to-neutral-600 font-medium text-white shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-zinc-800 dark:from-zinc-900 dark:to-zinc-900 dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
          type="button"
        >
          Sign up with Email &rarr;
          <span
            class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
          />
          <span
            class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
          />
        </button>
      </a>

      <div
        class="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-neutral-700"
      />

      <div class="flex flex-col space-y-4">
        <!-- GITHUB -->
        <a href={github_href}>
          <button
            class=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="button"
          >
            <IconBrandGithub class="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span class="text-sm text-neutral-700 dark:text-neutral-300"> GitHub </span>
            <span
              class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
            />
            <span
              class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
            />
          </button>
        </a>

        <!-- GOOGLE -->
        <a href={google_href}>
          <button
            class=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="button"
          >
            <IconBrandGoogle class="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span class="text-sm text-neutral-700 dark:text-neutral-300"> Google </span>
            <span
              class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
            />
            <span
              class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
            />
          </button>
        </a>

        <!-- SLACK -->
        <a href={slack_href}>
          <button
            class=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
            type="submit"
          >
            <IconBrandSlack class="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
            <span class="text-sm text-neutral-700 dark:text-neutral-300"> Slack </span>
            <span
              class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
            />
            <span
              class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
            />
          </button>
        </a>

        <!-- joke buttons down here -->

        <!-- ONLYFANS LMAO -->
        <button
          class=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
          type="submit"
        >
          <IconBrandOnlyfans class="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
          <span class="text-sm text-neutral-700 dark:text-neutral-300"> OnlyFans (coming soon) </span>
          <span
            class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
          />
          <span
            class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
          />
        </button>

        <!-- FORTNITE LMAO -->
        <button
          class=" group/btn relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black shadow-input dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_var(--neutral-800)]"
          type="submit"
        >
          <IconBrandFortnite class="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
          <span class="text-sm text-neutral-700 dark:text-neutral-300"> Fortnite (coming soon) </span>
          <span
            class="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100"
          />
          <span
            class="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100"
          />
        </button>
      </div>
    </div>
	</form>
</Dialog.Content>
