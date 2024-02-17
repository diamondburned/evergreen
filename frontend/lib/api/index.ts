import * as openapi from "$lib/api/openapi";
import { persisted } from "svelte-persisted-store";
import { derived } from "svelte/store";

openapi.defaults.credentials = "include";

export const token = persisted<string | null>("session-token", null);
token.subscribe((value) => {
  openapi.defaults.headers["Authorization"] = value ? `Bearer ${value}` : undefined;
});

export const isLoggedIn = derived(token, (token) => !!token);

export * from "$lib/api/openapi";
