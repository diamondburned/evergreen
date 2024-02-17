<script lang="ts">
  import "normalize.css/normalize.css";
  import "$lib/styles/material-css/theme.css";
  import "$lib/styles/main.scss";

  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { cubicIn, cubicOut } from "svelte/easing";
  import { token, createSession } from "$lib/api";

  export let data;

  const duration = 150;
  const delay = 20;
  const y = 10;

  const transitionIn = { easing: cubicOut, y, duration, delay: duration + delay };
  const transitionOut = { easing: cubicIn, y: -y, duration };

  let screenHeight = 0;

  onMount(async () => {
    if (!$token) {
      const session = await createSession();
      $token = session.token;
    }
  });
</script>

<svelte:window bind:innerHeight={screenHeight} />

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link
    href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap"
    rel="stylesheet"
  />
  <link rel="icon" type="image/png" href="/logo-small.png" />
</svelte:head>

<div class="background">
  {#key data.pathname}
    <div
      class="content"
      style="--screen-height: {screenHeight}px;"
      in:fly={transitionIn}
      out:fly={transitionOut}
    >
      <slot />
    </div>
  {/key}
</div>

<style lang="scss">
  div.background {
    background-color: var(--background);
    background-image: var(--background-gradient);
  }
  div.background,
  div.content {
    width: 100%;
    height: var(--screen-height, 100%);
  }
</style>
