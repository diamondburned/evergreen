<script lang="ts">
  import { fly } from "svelte/transition";
  import { isAuthorized, isLoggedIn } from "$lib/api";

  import Hero from "$lib/components/Hero.svelte";
  import LoadingDots from "$lib/components/LoadingDots.svelte";
</script>

<svelte:head>
  <title>Home</title>
</svelte:head>

<Hero>
  <div class="content">
    <hgroup>
      <img src="/logo.png" alt="Evergreen Logo" class="logo" />
      <h1 class="brand">Evergreen</h1>
    </hgroup>
    <div class="bottom">
      {#if !$isAuthorized}
        <div out:fly={{ y: -30, duration: 500 }}>
          <LoadingDots padded dotSize={24} distance={32} />
        </div>
      {:else}
        <div in:fly={{ y: 30, duration: 500, delay: 500 }}>
          <a role="button" class="large floaty inverted" href="/play">Play</a>
          <p class="alt-action">
            {#if $isLoggedIn}
              You are logged in. <a href="/dashboard">Go to Dashboard</a>
            {:else}
              Already played? <a href="/login">Sign in</a> or
              <a href="/dashboard">go to dashboard</a>
            {/if}
          </p>
        </div>
      {/if}
    </div>
  </div>
</Hero>

<style lang="scss">
  .content,
  .content > * {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .content {
    gap: 1rem;
    height: 100%;
    justify-content: space-evenly;
  }

  .logo {
    width: 200px;
    margin: auto;
  }

  .bottom {
    height: 5rem;
  }

  h1 {
    font-size: 3.5em;
    margin: 1rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
  }

  button,
  a[role="button"] {
    padding: 0.75em;
    width: 300px;
    max-width: 100%;

    font-size: 22px;

    border: none;
    border-radius: 15px;

    background-color: var(--primary);
    color: white;
  }

  p.alt-action {
    margin: 1rem auto;
    text-align: center;
    font-weight: 400;

    a {
      color: inherit;
      text-decoration: underline;
      font-weight: 600;
    }
  }
</style>
