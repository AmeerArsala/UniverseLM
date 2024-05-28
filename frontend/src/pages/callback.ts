import type { APIRoute } from "astro";
import axios from "axios";
import { BACKEND_URL } from "$lib/utils/envconfig";

export async function GET({params, request}) {
  // Call the post-register/login callback, which already has a RedirectResponse BUT WHO CARES
  // what matters is that it gets called so the backend knows
  let redirectRoute: string;

  try {
    const callbackMode: string = "smart";

    const callbackResponse = await axios.get(`${BACKEND_URL}/auth/kinde_callback/${callbackMode}`, {
      params: params
    });

    if (callbackResponse.data.is_first_time) {
      redirectRoute = "/";
    } else {
      redirectRoute = "/dashboard";
    }

    // put anything else you'd like to add here
  } catch (error) {
    console.log(error);

    redirectRoute = "/dashboard";
  }


  return new Response(null, {
    status: 308, // redirect status!!
    headers: {
      Location: redirectRoute,
    }
  });
}
