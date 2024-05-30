import { atom, map } from "nanostores";
import { persistentAtom, persistentMap } from "@nanostores/persistent";

// Web stores
export const numGitHubStars = atom(-1);

export const isAuthenticated = atom(false);
export const shouldCheckAuthentication = atom(true);

// App Stores
export const userID = persistentAtom("user_id", null);

// Core stores
export const community = atom({id: -1, name: ""});
