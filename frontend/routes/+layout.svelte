<script lang="ts">
  import "normalize.css/normalize.css";
  import "$lib/styles/material-css/theme.css";
  import "$lib/styles/main.scss";

  import { onMount } from "svelte";
  import { fly, fade } from "svelte/transition";
  import { cubicIn, cubicOut } from "svelte/easing";
  import { token, createSession } from "$lib/api";
  import { afterNavigate, beforeNavigate } from "$app/navigation";
  import LoadingDots from "$lib/components/LoadingDots.svelte";

  export let data;

  const duration = 150;
  const delay = 20;
  const y = 10;

  const transitionIn = { easing: cubicOut, y, duration, delay: duration + delay };
  const transitionOut = { easing: cubicIn, y: -y, duration };

  let screenHeight = 0;
  let loading = true;

  beforeNavigate(({ to }) => {
    if (to && to.route.id) {
      console.log("loading");
      loading = true;
    }
  });

  afterNavigate(() => {
    console.log("not loading");
    loading = false;
  });

  onMount(async () => {
    loading = false;
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
  {#if loading}
    <div class="loading-overlay" in:fly={transitionIn} out:fly={transitionOut}>
      <LoadingDots padded />
    </div>
  {/if}

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
  div.background,
  div.loading-overlay {
    background-color: var(--background);
    background-image: var(--background-gradient);
  }

  div.loading-overlay,
  div.background,
  div.content {
    width: 100%;
    height: var(--screen-height, 100%);
  }

  div.loading-overlay {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
</style>
