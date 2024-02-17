import * as openapi from "$lib/api/openapi";
export * from "$lib/api/openapi";

import { createSession } from "$lib/api/openapi";
import { persisted } from "svelte-persisted-store";
import { derived, readable, writable } from "svelte/store";

openapi.defaults.credentials = "include";
openapi.defaults.baseUrl = `/`;

export const token = persisted<string | null>("session-token", null);
token.subscribe((value) => {
  openapi.defaults.headers["Authorization"] = value ? `Bearer ${value}` : undefined;
});

export const isAuthorized = derived(token, (token) => token != null);
export const isLoggedIn = readable<boolean>(false);
