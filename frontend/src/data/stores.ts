import { atom, map } from "nanostores";
import { persistentAtom, persistentMap } from "@nanostores/persistent";

import { type Community } from "$lib/types/core";

// WEB STORES
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

// AUTH STORES
// Usually auth would not be persistent on purpose, but we can always re-run the auth check

// Auth states
export const authState = persistentAtom("auth_state");  // the actual STATE value from the authentication (a random string such as "BlueFox01")

// if user is registered with the core DB (Postgres)
const userRegistered = persistentAtom("is_core_registered");

export const coreRegistration = {
  isUserRegistered: (): boolean => (userRegistered.get() === 'true'),
  activateRegistration: () => {
    userRegistered.set('true');
  },
  // this is only for when the user logs out
  deactivateRegistration: () => {
    userRegistered.set('false');
  }
};

const authenticated = persistentAtom("is_authenticated");

export const authentication = {
  isAuthenticated: (): boolean => (authenticated.get() === 'true'),
  setIsAuthenticated: (value: boolean) => {
    authenticated.set(value.toString());
  },
  getAtom: () => authenticated
};

// APP STORES

// this is not to be confused with the user_id in the Postgres DB; this is for auth
// you can use this to derive the Postgres one
export const userAuthID = persistentAtom("user_id");

// CORE STORES
// stores relating to the core of the application
const user_core_id = persistentAtom("user_core_id"); // this one's an int

// probably don't RELY on this TOO much except as a cache. Functional is more secure
export const userCoreID = {
  getID: (): number => (parseInt(user_core_id.get())),
  setID: (id: number) => {
    user_core_id.set(id.toString());
  },
  getAtom: () => user_core_id
};

export const community = persistentAtom<Community>('active_community', {id: -1, name: ""}, {
  encode: JSON.stringify,
  decode: JSON.parse
});
