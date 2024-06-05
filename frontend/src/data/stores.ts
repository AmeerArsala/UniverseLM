import { atom, map } from "nanostores";
import { persistentAtom, persistentMap } from "@nanostores/persistent";

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

// auth is not persistent on purpose--oh wait we have shouldCheckAuthentication for that
export const authState = persistentAtom("auth_state");
const authenticated = persistentAtom("is_authenticated");

export const authentication = {
  isAuthenticated: (): boolean => (authenticated.get() === 'true'),
  setIsAuthenticated: (value: boolean) => {
    authenticated.set(value.toString());
  },
  getAtom: () => authenticated
};

export const shouldCheckAuthentication = atom(true);

// App Stores
export const userID = persistentAtom("user_id"); //, null);

// Core stores
// stores relating to the core of the application
export const community = atom({id: -1, name: ""});
