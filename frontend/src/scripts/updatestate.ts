import axios from "axios";
import Cookies from 'js-cookie';

import { REPO_URL } from "$lib/data/constants";
import { BACKEND_URL } from "$lib/data/envconfig";
import {
  githubStars,
  authState, authentication, coreRegistration, userAuthID,
  userCoreID
} from "$lib/data/stores";

// when to update all major values (where 'major' is defined by whether the whole site will break without correctly setting these values)
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
  console.log("userAuthID: " + userAuthID.get());

  // I FUCKING HATE JS WITH ITS BULLSHIT
  const MIN_ID_LENGTH: number = 3;
  const idNotFound = (id) => (id === null || id === undefined || id === "undefined" || id === "null" || id.length < MIN_ID_LENGTH);

  function onUserAuthIDNotFound() {
    console.log("No userAuthID found");
    authentication.setIsAuthenticated(false);
  }

  if (idNotFound(userAuthID.get())) {
    console.log("Trying again...");

    let user_auth_id = Cookies.get('user_id');
    console.log("userID (2nd attempt): " + user_auth_id);

    if (idNotFound(user_auth_id)) {
      console.log("Trying ONE more time...");

      console.log("Full cookie: " + document.cookie);
      user_auth_id = `; ${document.cookie}`.split(`; user_id=`);
      console.log(user_auth_id);

      if (idNotFound(user_auth_id)) {
        console.log("Ok, checking user_id via state");
        let state: string = authState.get();

        if (idNotFound(state)) {
          console.log("No state exists. Aborting.");
          return;
        }

        try {
          const response = await axios.get(`${BACKEND_URL}/auth/get_user_auth_id?state=${state}`);

          if (response.data === "NULL") {
            onUserAuthIDNotFound();
            return;
          } else {
            user_auth_id = response.data;
          }
        } catch(error) {
          onUserAuthIDNotFound();
          return;
        }
      }
    }

    userAuthID.set(user_auth_id); //localStorage.setItem("user_id", userAuthID);
    //Cookies.remove()
  }

  // update user authentication now
  console.log("Fetching authentication...");
  try {
    const response = await axios.get(`${BACKEND_URL}/auth/is_authenticated`, {
      params: {
        user_auth_id: userAuthID.get()
      }
    });
    authentication.setIsAuthenticated(response.data);

    console.log("Authentication Fetched! Authenticated: " + authentication.isAuthenticated());
    postAuthentication();
  } catch(error) {
    console.log("ERROR FINDING OUT WHETHER USER IS AUTHENTICATED:");
    console.log(error);

    authentication.setIsAuthenticated(false);
  }
}

function postAuthentication() {
  if (!coreRegistration.isUserRegistered()) {
    // Call the route to manifest the user
    axios.post(`${BACKEND_URL}/user/manifest`, {
      params: {
        user_auth_id: userAuthID.get()
      }
    }, {
      withCredentials: true
    }).then((response) => {
      userCoreID.setID(response.data);
    }).catch((error) => {
      console.log("Error manifesting user:\n" + error);
    });

    // activate the registration
    coreRegistration.activateRegistration();
  }
}
