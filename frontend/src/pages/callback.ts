import type { APIRoute } from "astro";

export async function GET({params, request}) {
  // TODO: do stuff here

  return new Response(null, {
    status: 308, // redirect status!!
    headers: {
      Location: '/',
    }
  });
}
