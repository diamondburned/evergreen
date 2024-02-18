// vite.config.ts
import { defineConfig } from "file:///Users/ez/Desktop/pixiecode/node_modules/vite/dist/node/index.js";
import { sveltekit } from "file:///Users/ez/Desktop/pixiecode/node_modules/@sveltejs/kit/src/exports/vite/index.js";
import "file:///Users/ez/Desktop/pixiecode/node_modules/vite-plugin-run/dist/index.mjs";
var vite_config_default = defineConfig({
  clearScreen: false,
  // fuck Vite lol
  plugins: [
    sveltekit()
    // run({
    //   input: {
    //     name: "generate OpenAPI client",
    //     run: ["node", "utils/generate-openapi.js"],
    //     pattern: ["**/*.py"],
    //     startup: true,
    //     build: true,
    //   },
    //   silent: false,
    // }),
  ],
  server: {
    host: true,
    port: 3e3,
    proxy: {
      "/api": process.env.API_ENDPOINT || ""
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvZXovRGVza3RvcC9waXhpZWNvZGVcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9Vc2Vycy9lei9EZXNrdG9wL3BpeGllY29kZS92aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vVXNlcnMvZXovRGVza3RvcC9waXhpZWNvZGUvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tIFwidml0ZVwiO1xuaW1wb3J0IHsgc3ZlbHRla2l0IH0gZnJvbSBcIkBzdmVsdGVqcy9raXQvdml0ZVwiO1xuaW1wb3J0IHsgcnVuIH0gZnJvbSBcInZpdGUtcGx1Z2luLXJ1blwiO1xuXG4vLyBodHRwczovL2dpdGh1Yi5jb20vdml0ZWpzL3ZpdGUvaXNzdWVzLzczODUjaXNzdWVjb21tZW50LTEyODY2MDYyOThcbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIGNsZWFyU2NyZWVuOiBmYWxzZSwgLy8gZnVjayBWaXRlIGxvbFxuICBwbHVnaW5zOiBbXG4gICAgc3ZlbHRla2l0KCksXG4gICAgLy8gcnVuKHtcbiAgICAvLyAgIGlucHV0OiB7XG4gICAgLy8gICAgIG5hbWU6IFwiZ2VuZXJhdGUgT3BlbkFQSSBjbGllbnRcIixcbiAgICAvLyAgICAgcnVuOiBbXCJub2RlXCIsIFwidXRpbHMvZ2VuZXJhdGUtb3BlbmFwaS5qc1wiXSxcbiAgICAvLyAgICAgcGF0dGVybjogW1wiKiovKi5weVwiXSxcbiAgICAvLyAgICAgc3RhcnR1cDogdHJ1ZSxcbiAgICAvLyAgICAgYnVpbGQ6IHRydWUsXG4gICAgLy8gICB9LFxuICAgIC8vICAgc2lsZW50OiBmYWxzZSxcbiAgICAvLyB9KSxcbiAgXSxcbiAgc2VydmVyOiB7XG4gICAgaG9zdDogdHJ1ZSxcbiAgICBwb3J0OiAzMDAwLFxuICAgIHByb3h5OiB7XG4gICAgICBcIi9hcGlcIjogcHJvY2Vzcy5lbnYuQVBJX0VORFBPSU5UIHx8IFwiXCIsXG4gICAgfSxcbiAgfSxcbn0pO1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFtUSxTQUFTLG9CQUFvQjtBQUNoUyxTQUFTLGlCQUFpQjtBQUMxQixPQUFvQjtBQUdwQixJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixhQUFhO0FBQUE7QUFBQSxFQUNiLFNBQVM7QUFBQSxJQUNQLFVBQVU7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLEVBV1o7QUFBQSxFQUNBLFFBQVE7QUFBQSxJQUNOLE1BQU07QUFBQSxJQUNOLE1BQU07QUFBQSxJQUNOLE9BQU87QUFBQSxNQUNMLFFBQVEsUUFBUSxJQUFJLGdCQUFnQjtBQUFBLElBQ3RDO0FBQUEsRUFDRjtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
