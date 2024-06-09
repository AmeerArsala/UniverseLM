import { atom, map } from "nanostores";
import { type UserDetails, retrieveUserDetails } from "$lib/data/datafunctions";

export const userDetails = atom<UserDetails>({
  given_name: "John",
  id: "",
  family_name: "Doe",
  email: "john.doe@example.com",
  picture: "/images/default_user.png" // public
});
export const userREADMEmd = atom("");
export const userTierPlan = atom('FREE');
