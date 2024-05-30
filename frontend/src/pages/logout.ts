import type { APIRoute } from "astro";
import axios from "axios";
import { BACKEND_URL } from "$lib/data/envconfig";

// These files execute on the server and are API Endpoints
export async function GET({params, request}) {
  // put anything else you'd like to add here
  console.log('hiii');


  return new Response(null, {
    status: 308, // redirect status!!
    headers: {
      Location: "/",
    }
  });
}
