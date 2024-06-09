import axios from "axios";
import { BACKEND_URL } from "./envconfig";
import { userCoreID, userAuthID, apiKey, authentication, coreRegistration } from "./stores";

const MIN_ID_LENGTH: number = 3;
export const idNotFound = (id): boolean => (id === null || id === undefined || id === "undefined" || id === "null" || id.length < MIN_ID_LENGTH);

export function hasAPIKey(): boolean {
  return !idNotFound(apiKey.get());
}

// reset state
export function onLogout() {
  userAuthID.set("undefined");
  authentication.setIsAuthenticated(false);
  coreRegistration.deactivateRegistration();
}

export async function retrieveUserCoreID() {
  try {
    const response = await axios.get(`${BACKEND_URL}/user/${userAuthID.get()}/view_details/user_core_id`, {
      withCredentials: true
    });

    let userID: number = response.data;

    // update the state of userCoreID
    userCoreID.setID(userID);
    return userID;
  } catch (error) {
    console.log("Error retrieving user core id: " + error);
  }
}

export async function retrieveUserEmail() {
  try {
    const response = await axios.get(`${BACKEND_URL}/user/${userAuthID.get()}/view_details/email`, {
      withCredentials: true
    });

    let userEmail: string = response.data;
    return userEmail;
  } catch (error) {
    console.log("Error retrieving user email: " + error);
  }
}

export interface UserDetails {
  given_name: string,  // first name
  id: string,          // auth id
  family_name: string, // last name
  email: string,       // email
  picture: string      // link to image
};

export async function retrieveUserDetails() {
  try {
    const response = await axios.get(`${BACKEND_URL}/user/${userAuthID.get()}/view_details`, {
      withCredentials: true
    });

    let userDetails: UserDetails = response.data;
    return userDetails;
  } catch (error) {
    console.log("Error retrieving user details: " + error);
  }
}

export async function retrieveAPIKey() {
  try {
    const response = await axios.post(`${BACKEND_URL}/user/${userAuthID.get()}/get_apikey`, {
      params: {}
    }, {
      withCredentials: true
    });

    const API_KEY: string = response.data;

    // Update stored api key
    apiKey.set(API_KEY);
    return API_KEY;
  } catch (error) {
    console.log("Error retrieving user api key: " + error);
  }
}
