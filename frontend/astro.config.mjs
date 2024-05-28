import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import svelte from "@astrojs/svelte";
import react from "@astrojs/react";
import mdx from "@astrojs/mdx";
import node from "@astrojs/node";
import vercel from "@astrojs/vercel/serverless";
import webVitals from "@astrojs/web-vitals";

import sentry from "@sentry/astro";
import spotlightjs from "@spotlightjs/astro";

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind({
    applyBaseStyles: false
  }), svelte(), react(), mdx()],
  output: "hybrid",
  adapter: vercel(),
  redirects: {
    "/logout": "/", // Logging out redirects back to homepage
    // also make the login/register redirection to be dynamic such that:
    // any typical login would take straight to the dashboard
    // whereas registration takes to the homepage
  }
});
