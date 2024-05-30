import axios from "axios";
import Cookies from 'js-cookie';

import { REPO_URL } from "$lib/data/constants";
import { BACKEND_URL } from "$lib/data/envconfig";
import { numGitHubStars, isAuthenticated, shouldCheckAuthentication, userID } from "$lib/data/stores";

// when to update all major values
export default async function update() {
  if (shouldCheckAuthentication.get()) {
    await updateAuthenticationState();
    shouldCheckAuthentication.set(false);
  }
}

export async function updateAll() {
  await updateStargazers();
  await updateAuthenticationState();
}

export async function updateStargazers(repo_link: string = REPO_URL) {
  let stars = numGitHubStars.get();

  console.log("Fetching stargazers...");

  const prefixLength = ("https://github.com/").length;
  let repo_id: string = repo_link.substring(prefixLength);

  const response = await fetch(`https://api.github.com/repos/${repo_id}`);

  if (response.ok) {
    const data = await response.json();
    stars = data.stargazers_count;
    numGitHubStars.set(data.stargazers_count);
    console.log("stargazers (fetched): " + stars);
  } else {
    console.error("Failed to fetch repository data");
  }

  //return stars;
}

export async function updateAuthenticationState() {
  console.log("Updating authentication state...");

  // retrieve state of user ID
  console.log("Getting ID...");
  console.log("userID: " + userID.get());

  /*console.log(userID === undefined);
  console.log(typeof userID === "undefined");
  console.log(userID === void 0);
  console.log(userID === null);
  console.log(userID.length);*/

  // I FUCKING HATE JS WITH ITS BULLSHIT
  const idNotFound = (id) => (id === null || id === "undefined" || id === "null");

  if (idNotFound(userID.get())) {
    console.log("Trying again...");

    let cookieUserID = Cookies.get('user_id');
    console.log("userID (2nd attempt): " + cookieUserID);

    if (idNotFound(cookieUserID)) {
      console.log("No userID found");
      isAuthenticated.set(false);
      return;
    }

    userID.set(cookieUserID); //localStorage.setItem("user_id", userID);
    //Cookies.remove()
  }

  //const userId: string = localStorage.getItem('userId');

  // update user authentication state now
  console.log("Fetching authentication state...");
  try {
    const response = await axios.get(`${BACKEND_URL}/auth/is_authenticated`, {
      params: {
        user_id: userID.get()
      }
    });
    isAuthenticated.set(response.data);

    console.log("Authentication State Fetched! Authenticated: " + isAuthenticated.get());
  } catch(error) {
    console.log("ERROR FINDING OUT WHETHER USER IS AUTHENTICATED:");
    console.log(error);

    isAuthenticated.set(false);
  }
}
