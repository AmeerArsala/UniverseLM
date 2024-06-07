import axios from "axios";
import { BACKEND_URL } from "./envconfig";
import { userCoreID } from "./stores";

export async function retrieveUserCoreID() {
  try {
    const response = await axios.get(`${BACKEND_URL}/user/view_details/user_core_id`, {
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
    const response = await axios.get(`${BACKEND_URL}/user/view_details/email`, {
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
    const response = await axios.get(`${BACKEND_URL}/user/view_details`, {
      withCredentials: true
    });

    let userDetails: UserDetails = response.data;
    return userDetails;
  } catch (error) {
    console.log("Error retrieving user details: " + error);
  }
}
