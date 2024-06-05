<script lang="ts">
  import { onMount } from "svelte";
  import { Input } from "$lib/components/ui/input";
  import * as Table from "$lib/components/ui/table";
  import * as Collapsible from "$lib/components/ui/collapsible";
  import { Button } from "$lib/components/ui/button";
  import PreviewAndJoinCommunities from "./PreviewAndJoinCommunities.svelte";
  import DensityView from "./DensityView.svelte";

  import { readable } from "svelte/store";
  //import ArrowUpDown from "lucide-svelte/icons/arrow-up-down";
  //import ChevronDown from "lucide-svelte/icons/chevron-down";
  import { cn } from "$lib/utils.js";

  import {
    Render,
    Subscribe,
    createRender,
    createTable
  } from "svelte-headless-table";
  import {
    addHiddenColumns,
    addPagination,
    addSelectedRows,
    addSortBy,
    addTableFilter
  } from "svelte-headless-table/plugins";

  // Mock data
  import mockData from "$lib/data/mocked_communities.json";

  export let maxInPreview = 5;  // max results shown in preview
  export let maxInExpandedPreview = 10;
  let expanded: boolean = false;

  type CommunityOverview = {
    id: number;
    name: string;
    stddevs_from_mean_lore_density: number;
  };

  let communities: CommunityOverview[] = mockData.communities;

  onMount(() => {
    // For now, set communities to some dummy data (11 fake communities). Otherwise, call the backend to pull from a DB
    communities = mockData.communities;

    //TODO: interface with api for communities data
  });

  const table = createTable(readable(communities), {
    sort: addSortBy({ disableMultiSort: true }),
    page: addPagination({initialPageSize: maxInPreview}),
    filter: addTableFilter({
      fn: ({ filterValue, value }) => value.includes(filterValue)
    })
  });

  const columns = table.createColumns([
    table.column({
      header: "Community",
      accessor: "name",
      cell: ({ value }) => value.toLowerCase(),
      plugins: {
        filter: {
          getFilterValue(value) {
            return value.toLowerCase();
          }
        }
      }
    }),
    table.column({
      header: "Density",
      accessor: "stddevs_from_mean_lore_density",
      cell: (item) => {
        return createRender(DensityView, { density: item.value });
      },
      plugins: { sort: { disable: true }, filter: { exclude: true } }
    }),
    table.column({
      header: "", // This column holds the preview and join buttons
      accessor: ({ id }) => id,
      cell: (item) => {
        return createRender(PreviewAndJoinCommunities);
      },
      plugins: { sort: { disable: true } }
    })
  ]);

  const {
    headerRows,
    pageRows,
    tableAttrs,
    tableBodyAttrs,
    flatColumns,
    pluginStates,
    rows
  } = table.createViewModel(columns);

  const { sortKeys } = pluginStates.sort;
  //const ids = flatColumns.map((c) => c.id);

  const { hasNextPage, hasPreviousPage, pageIndex, pageSize } = pluginStates.page;
  const { filterValue } = pluginStates.filter;

  function toggleExpansion() {
    expanded = !expanded;

    if (expanded) {
      pageSize.set(maxInExpandedPreview);
    } else {
      pageSize.set(maxInPreview);
    }
  }


</script>

<div class="w-full">
  <div class="flex items-center justify-center py-4">
    <Input
      class="w-full"
      placeholder="Filter Communities..."
      type="text"
      bind:value={$filterValue}
    />
  </div>
  <div class="rounded-md border bg-background">
    <Table.Root {...$tableAttrs}>
      <!--TABLE HEADER-->
      <Table.Header>
        {#each $headerRows as headerRow}
          <Subscribe rowAttrs={headerRow.attrs()}>
            <Table.Row>
              {#each headerRow.cells as cell (cell.id)}
                <Subscribe
                  attrs={cell.attrs()}
                  let:attrs
                  props={cell.props()}
                  let:props
                >
                  <Table.Head
                    {...attrs}
                    class={cn("[&:has([role=checkbox])]:pl-3")}
                  >
                    <Render of={cell.render()} />
                  </Table.Head>
                </Subscribe>
              {/each}
            </Table.Row>
          </Subscribe>
        {/each}
      </Table.Header>

      <!--TABLE BODY-->
      <Table.Body {...$tableBodyAttrs}>
        {#each $pageRows as row (row.id)}
          <Subscribe rowAttrs={row.attrs()} let:rowAttrs>
            <Table.Row
              {...rowAttrs}
            >
              {#each row.cells as cell (cell.id)}
                <Subscribe attrs={cell.attrs()} let:attrs>
                  <Table.Cell class="[&:has([role=checkbox])]:pl-3" {...attrs}>
                    <Render of={cell.render()} />
                  </Table.Cell>
                </Subscribe>
              {/each}
            </Table.Row>
          </Subscribe>
        {/each}
      </Table.Body>

    </Table.Root>
  </div>
  <div class="flex items-center justify-end space-x-2 py-4">
    <Button
      class="mr-auto"
      variant="outline"
      size="sm"
      on:click={toggleExpansion}>
      {expanded ? "Show Less" : "Show More"}
    </Button>

    <Button
      variant="outline"
      size="sm"
      on:click={() => ($pageIndex = $pageIndex - 1)}
      disabled={!$hasPreviousPage}>Previous</Button
    >
    <Button
      variant="outline"
      size="sm"
      disabled={!$hasNextPage}
      on:click={() => ($pageIndex = $pageIndex + 1)}>Next</Button
    >
  </div>
</div>
