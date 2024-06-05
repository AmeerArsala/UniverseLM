import axios from "axios";
import Cookies from 'js-cookie';

import { REPO_URL } from "$lib/data/constants";
import { BACKEND_URL } from "$lib/data/envconfig";
import { githubStars, authState, authentication, userID } from "$lib/data/stores";

// when to update all major values
export default async function update() {
  await updateAuthentication();
}

export async function updateStargazers(repo_link: string = REPO_URL) {
  let stars: number = githubStars.getNum();

  console.log("Fetching stargazers...");

  const prefixLength = ("https://github.com/").length;
  let repo_id: string = repo_link.substring(prefixLength);

  const response = await fetch(`https://api.github.com/repos/${repo_id}`);

  if (response.ok) {
    const data = await response.json();
    stars = data.stargazers_count;
    githubStars.setNum(data.stargazers_count);
    console.log("stargazers (fetched): " + stars);
  } else {
    console.error("Failed to fetch repository data");
  }

  return stars;
}

export async function updateAuthentication() {
  console.log("Updating authentication value...");

  // retrieve state of user ID
  console.log("Getting ID...");
  console.log("userID: " + userID.get());

  /*console.log(userID === undefined);
  console.log(typeof userID === "undefined");
  console.log(userID === void 0);
  console.log(userID === null);
  console.log(userID.length);*/

  // I FUCKING HATE JS WITH ITS BULLSHIT
  const MIN_ID_LENGTH: number = 3;
  const idNotFound = (id) => (id === null || id === undefined || id === "undefined" || id === "null" || id.length < MIN_ID_LENGTH);

  if (idNotFound(userID.get())) {
    console.log("Trying again...");

    let user_id = Cookies.get('user_id');
    console.log("userID (2nd attempt): " + user_id);

    if (idNotFound(user_id)) {
      console.log("Trying ONE more time...");

      console.log("Full cookie: " + document.cookie);
      user_id = `; ${document.cookie}`.split(`; user_id=`);
      console.log(user_id);

      if (idNotFound(user_id)) {
        console.log("Ok, checking user_id via state");
        let state: string = authState.get();

        try {
          const response = await axios.get(`${BACKEND_URL}/auth/get_user_id?state=${state}`);

          user_id = response.data;
        } catch(error) {
          console.log("No userID found");
          authentication.setIsAuthenticated(false);
          return;
        }
      }
    }

    userID.set(user_id); //localStorage.setItem("user_id", userID);
    //Cookies.remove()
  }

  //const userId: string = localStorage.getItem('userId');

  // update user authentication now
  console.log("Fetching authentication...");
  try {
    const response = await axios.get(`${BACKEND_URL}/auth/is_authenticated`, {
      params: {
        user_id: userID.get()
      }
    });
    authentication.setIsAuthenticated(response.data);

    console.log("Authentication Fetched! Authenticated: " + authentication.isAuthenticated());
  } catch(error) {
    console.log("ERROR FINDING OUT WHETHER USER IS AUTHENTICATED:");
    console.log(error);

    authentication.setIsAuthenticated(false);
  }
}
