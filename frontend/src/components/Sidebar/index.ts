import StandardSidebar from "./StandardSidebar.svelte";
import Sidebar from "./Sidebar.svelte";


interface SidebarItem {
  text: string,
  iconComponent: any, // idk what the svelte component type is
  href: string,
  target: "_blank" | "_self" | "_parent" | "_top",
};

export {
  type SidebarItem,
  StandardSidebar,
  Sidebar
};
