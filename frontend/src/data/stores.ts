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

// auth is not persistent on purpose
export const isAuthenticated = atom(false);
export const shouldCheckAuthentication = atom(true);

// App Stores
export const userID = persistentAtom("user_id"); //, null);

// Core stores
// stores relating to the core of the application
export const community = atom({id: -1, name: ""});
