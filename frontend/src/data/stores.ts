import { atom, map } from "nanostores";
import { persistentAtom, persistentMap } from "@nanostores/persistent";

// Web stores
const numGitHubStars = persistentAtom("num_github_stars", "-1");

export const githubStars = {
  getNum: (): number => {
    return parseInt(numGitHubStars.get());
  },
  setNum: (stars: number) => { numGitHubStars.set(stars.toString()); }
};


export const isAuthenticated = atom(false);
export const shouldCheckAuthentication = atom(true);

// App Stores
export const userID = persistentAtom("user_id", null);

// Core stores
export const community = atom({id: -1, name: ""});
