import { atom, map } from "nanostores";
import { persistentAtom, persistentMap } from "@nanostores/persistent";

import { type Community } from "$lib/types/core";

// Web stores
const numGitHubStars = persistentAtom("num_github_stars");

export const githubStars = {
  getNum: (): number => {
    return parseInt(numGitHubStars.get());
  },
  setNum: (stars: number) => {
    numGitHubStars.set(stars.toString());
  },
  getAtom: () => numGitHubStars
};

// Usually auth would not be persistent on purpose, but we can always re-run the auth check
export const authState = persistentAtom("auth_state");  // the actual STATE value from the authentication (a random string such as "BlueFox01")
const authenticated = persistentAtom("is_authenticated");

export const authentication = {
  isAuthenticated: (): boolean => (authenticated.get() === 'true'),
  setIsAuthenticated: (value: boolean) => {
    authenticated.set(value.toString());
  },
  getAtom: () => authenticated
};

// App Stores
export const userID = persistentAtom("user_id"); //, null);

// Core stores
// stores relating to the core of the application
export const community = persistentAtom<Community>('active_community', {id: -1, name: ""}, {
  encode: JSON.stringify,
  decode: JSON.parse
});
