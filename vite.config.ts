import { defineConfig } from "vite";
import { sveltekit } from "@sveltejs/kit/vite";
import { run } from "vite-plugin-run";

// https://github.com/vitejs/vite/issues/7385#issuecomment-1286606298
export default defineConfig({
  clearScreen: false, // fuck Vite lol
  plugins: [
    sveltekit(),
    run({
      input: {
        name: "generate OpenAPI client",
        run: ["node", "utils/generate-openapi.js"],
        pattern: ["**/*.py"],
        startup: true,
        build: true,
      },
      silent: false,
    }),
  ],
  server: {
    host: true,
    port: 3000,
    proxy: {
      "/api": process.env.API_ENDPOINT || "",
    },
  },
});
