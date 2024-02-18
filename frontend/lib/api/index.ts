import { goto } from "$app/navigation";
import * as openapi from "$lib/api/openapi";
export * from "$lib/api/openapi";

import { persisted } from "svelte-persisted-store";
import { derived } from "svelte/store";

openapi.defaults.credentials = "include";
openapi.defaults.baseUrl = `/`;
openapi.defaults.fetch = async (input, init) => {
  const response = await fetch(input, init);
  if (response.status === 401) {
    token.set(null);
    isLoggedIn.set(false);

    // Hard redirect to the homepage to obtain a new token.
    if (window.location.pathname !== "/") {
      window.location.href = "/";
    }
  }

  return response;
};

export const token = persisted<string | null>("session-token", null);
token.subscribe((value) => {
  openapi.defaults.headers["Authorization"] = value ? `Bearer ${value}` : undefined;
});

export const isAuthorized = derived(token, (token) => token != null);
export const isLoggedIn = persisted<boolean>("logged-in", false);
