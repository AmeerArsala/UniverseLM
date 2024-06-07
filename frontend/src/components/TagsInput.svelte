<script lang="ts">
  import { onMount } from 'svelte';
  import { createTagsInput, melt } from '@melt-ui/svelte';
  import X$1 from '@tabler/icons-svelte/IconX.svelte';

  import { Input } from "$lib/components/ui/input/index.js";

  export let defaultTags: string[] = [];
  export let unique: boolean = true;

  export let placeholderText: string = "Enter tags...";

  export let tag_names: string[] = [...defaultTags];

  const {
    elements: { root, input, tag, deleteTrigger, edit },
    states: { tags },
  } = createTagsInput({
    defaultTags: defaultTags,
    unique: unique,
    add(tag) {
      return { id: tag, value: tag };
    },
    addOnPaste: true,
  });

  onMount(() => {
    tags.subscribe((values) => {
      // update tag_names every time
      tag_names = [];
      for (let i = 0; i < values.length; ++i) {
        tag_names.push(values[i].value);
      }
    });
  });
</script>

<div class="flex flex-col items-start justify-center gap-2">
  <div
    use:melt={$root}
    class="flex min-w-[280px] flex-row flex-wrap gap-2.5 rounded-md bg-black border-solid border-[1px] px-3 py-2 text-magnum-700
    focus-within:ring focus-within:ring-magnum-400"
  >
    {#each $tags as t}
      <div
        use:melt={$tag(t)}
        class="flex items-center overflow-hidden rounded-md bg-magnum-200 text-magnum-900 [word-break:break-word] data-[disabled]:bg-magnum-300 bg-indigo-600 data-[selected]:bg-magnum-400 data-[disabled]:hover:cursor-default data-[disabled]:focus:!outline-none data-[disabled]:focus:!ring-0"
      >
        <span class="flex items-center border-r border-white/10 px-1.5 text-sm"
          >{t.value}</span
        >
        <button
          use:melt={$deleteTrigger(t)}
          class="flex h-full items-center px-1 enabled:hover:bg-magnum-300"
        >
          <!-- if this doesn't work, just use the letter 'x' -->
          <X$1 class="size-3" />
        </button>
      </div>
      <div
        use:melt={$edit(t)}
        class="flex items-center overflow-hidden rounded-md px-1.5 [word-break:break-word] data-[invalid-edit]:focus:!ring-indigo-600"
      />
    {/each}

    <!-- Switch back to regular `input` if this doesn't work -->
    <input
      use:melt={$input}
      type="text"
      placeholder={placeholderText}
      class="min-w-[17.5rem] shrink grow basis-0 border-0 bg-black text-white outline-none text-sm focus:!ring-0 data-[invalid]:text-indigo-600"
    />
  </div>
</div>
