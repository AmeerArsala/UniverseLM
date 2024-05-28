// Will be true on prod
export const PROD_MODE: boolean = (process.env.MODE === "PROD");

// Local dev params
export const SITE_HOST: string = "localhost";
export const SITE_PORT: number = 4321;

export const SITE_URL: string = PROD_MODE ? "https://universelm.org" : `http://${SITE_HOST}:${SITE_PORT}`;

export const DEV_BACKEND: string = "http://localhost:8080";
export const BACKEND_URL: string = PROD_MODE ? process.env.BACKEND_URL : DEV_BACKEND;
