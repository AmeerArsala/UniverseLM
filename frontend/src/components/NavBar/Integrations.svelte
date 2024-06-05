<script lang="ts">
  import { MenuItem, ProductItem, HoveredLink } from "@components/ui/NavbarMenu";

  let active: string | null = null;
</script>

<MenuItem {active} item="Integrations">
  <div class="grid grid-cols-1 gap-3 p-0 text-sm">
    <ProductItem
      title="Discord Bot"
      href="/integrations/discord"
      src="/discord.png"
    />
    <ProductItem
      title="Slack Bot"
      href="/integrations/slack"
      src="/slack.png"
    />
    <ProductItem
      title="CLI"
      href="/cli"
      src="/cli_clipart.png"
    />
  </div>
</MenuItem>
