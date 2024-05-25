import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import svelte from "@astrojs/svelte";
import react from "@astrojs/react";
import mdx from "@astrojs/mdx";

import node from "@astrojs/node";
import vercel from "@astrojs/vercel/serverless";

import webVitals from "@astrojs/web-vitals";

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind({
    applyBaseStyles: false
  }), svelte(), react(), mdx()],
  output: "hybrid",
  adapter: vercel()
});
